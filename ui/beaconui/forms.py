import logging
from urllib.parse import urlencode
import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings

from . import conf

LOG = logging.getLogger(__name__)


###########################################################################
### For the regular queries
###########################################################################

variantTypes = ('DEL:ME','INS:ME','DUP:TANDEM','DUP','DEL','INS','INV','CNV','SNP','MNP')
regex = re.compile(r'^(X|Y|MT|[1-9]|1[0-9]|2[0-2])\s*\:\s*(\d+)\s+([ATCGN]+)\s*\>\s*(DEL:ME|INS:ME|DUP:TANDEM|DUP|DEL|INS|INV|CNV|SNP|MNP|[ATCGN]+)$', re.I)


# class IncludeDatasetResponsesWidget(forms.RadioSelect):
#     template_name='forms/include_dataset_responses.html'

        
class QueryForm(forms.Form):

    assemblyId = forms.ChoiceField(required=True,
                                   choices=( (i,i) for i in conf.BEACON_ASSEMBLYIDS ),
                                   error_messages = { 'invalid_choice': ('<p>Select a valid choice.</p>'
                                                                         '<p>%(value)s is not one of the available choices.</p>'),
                                                      'required': '<p>is required</p>' },
                                   label='Assembly Id')

    query = forms.CharField(
        strip=True,
        required=True,
        label=mark_safe('Chromosome : Position ReferenceBase &gt; (AlternateBase|VariantType)'),
        label_suffix = '',
        error_messages = { 'required': "<p>Eh? ... What was the query again?</p>"},
        widget=forms.TextInput(attrs={'data-lpignore':'true', # data-lpignore=true to ignore LastPass injected code
                                      'placeholder': 'For example  10 : 12345 A > T'}),
    )
    

    includeDatasetResponses = forms.ChoiceField(required=True,
                                                choices=( (i.upper(),i) for i in ('All','Hit','Miss','None') ),
                                                label='Included Dataset Responses',
                                                widget=forms.Select,  # instead of IncludeDatasetResponsesWidget
                                                initial='ALL')
    
    print(includeDatasetResponses)
    def is_valid(self):
        self.full_clean() # Populate fields (or read self.errors)

        # Short circuit already 
        if not super().is_valid():
            return False

        query = self.cleaned_data.get('query')
        LOG.debug('Query: %s', query)

        # So far so good
        self.query_deconstructed_data = None

        # Testing the regular Query
        m = regex.match(query)
        if m:
            d = { 'referenceName': m.group(1),
                  'start': m.group(2),
                  'referenceBases': m.group(3),
                  'includeDatasetResponses': self.cleaned_data.get('includeDatasetResponses'),
                  'assemblyId': self.cleaned_data.get('assemblyId') 
            }
            v = m.group(4)
            k = 'variantType' if v in variantTypes else 'alternateBases'
            d[k] = v
            self.query_deconstructed_data = d
            return True

        # Invalid query
        self.add_error('query', ValidationError(_('<p><span class="bold">Oops! </span>Query <code>%(value)s</code> must be of the form:</p>'
                                                  '<p><span class="query-form">Regular Query</span>Chromosome : Position ReferenceBase &gt; (AlternateBase|VariantType)</p>'
                                                  '<div class="small">'
                                                  '<p>where</p>'
                                                  '<ul>'
                                                  '<li>- Chromosome: 1-22, X, Y, or MT</li>'
                                                  '<li>- Position: a positive integer</li>'
                                                  '<li>- VariantType: either DEL:ME, INS:ME, DUP:TANDEM, DUP, DEL, INS, INV, CNV, SNP, or MNP</li>'
                                                  '<li>- ReferenceBase or AlternateBase: a combination of one or more A, T, C, G, or N</li>'
                                                  '</ul>'
                                                  '</div>'),
                                                params={'value':query}))

        return False

###########################################################################
### For the region queries
###########################################################################

region_regex = re.compile(r'^(X|Y|MT|[1-9]|1[0-9]|2[0-2])\s*\:\s*(\d+)\s*-\s*(\d+)$', re.I)

class QueryRegionForm(forms.Form):

    assemblyId = forms.ChoiceField(required=True,
                                   choices=( (i,i) for i in conf.BEACON_ASSEMBLYIDS ),
                                   error_messages = { 'invalid_choice': ('<p>Select a valid choice.</p>'
                                                                         '<p>%(value)s is not one of the available choices.</p>'),
                                                      'required': '<p>is required</p>' },
                                   label='Assembly Id')

    query = forms.CharField(
        strip=True,
        required=True,
        label=mark_safe('Chromosome : Start-End'),
        label_suffix = '',
        error_messages = { 'required': "<p>Eh? ... What was the query again?</p>"},
        widget=forms.TextInput(attrs={'data-lpignore':'true', # data-lpignore=true to ignore LastPass injected code
                                      'placeholder': 'For example  10 : 1234 - 5678'}),
    )

    includeDatasetResponses = forms.ChoiceField(required=True,
                                                choices=( (i.upper(),i) for i in ('All','Hit','Miss','None') ),
                                                label='Included Dataset Responses',
                                                widget=forms.Select,  # instead of IncludeDatasetResponsesWidget
                                                initial='NONE')    

    def is_valid(self):
        self.full_clean() # Populate fields (or read self.errors)

        # Short circuit already 
        if not super().is_valid():
            return False

        query = self.cleaned_data.get('query')
        LOG.debug('Query: %s', query)

        # So far so good
        self.query_deconstructed_data = None

        # Testing for Region Query
        m = region_regex.match(query)
        if m: # Correct Region Query
            self.query_deconstructed_data = { 'referenceName': m.group(1),
                                              'start': m.group(2),
                                              'end': m.group(3),
                                              'includeDatasetResponses': self.cleaned_data.get('includeDatasetResponses'),
                                              'assemblyId': self.cleaned_data.get('assemblyId') 
            }
            return True

        # Invalid query
        self.add_error('query', ValidationError(_('<p><span class="bold">Oops! </span>Query <code>%(value)s</code> must be of the form:</p>'
                                                  '<p><span class="query-form">Region Query</span>Chromosome : Start-End</p>'
                                                  '<div class="small">'
                                                  '<p>where</p>'
                                                  '<ul>'
                                                  '<li>- Chromosome is either 1-22, X, Y, or MT</li>'
                                                  '<li>- Start, End are positive integers</li>'
                                                  '</ul>'
                                                  '</div>'),
                                                params={'value':query}))

        return False

###########################################################################
### For the samples queries
###########################################################################

variantTypes = ('DEL:ME','INS:ME','DUP:TANDEM','DUP','DEL','INS','INV','CNV','SNP','MNP')
regex = re.compile(r'^(X|Y|MT|[1-9]|1[0-9]|2[0-2])\s*\:\s*(\d+)\s+([ATCGN]+)\s*\>\s*(DEL:ME|INS:ME|DUP:TANDEM|DUP|DEL|INS|INV|CNV|SNP|MNP|[ATCGN]+)$', re.I)
        
class QuerySamplesForm(forms.Form):

    assemblyId = forms.ChoiceField(required=False,
                                   choices=( (i,i) for i in conf.BEACON_ASSEMBLYIDS ),
                                   error_messages = { 'invalid_choice': ('<p>Select a valid choice.</p>'
                                                                         '<p>%(value)s is not one of the available choices.</p>'),
                                                      'required': '<p>is required</p>' },
                                   label='Assembly Id')

    query = forms.CharField(
        strip=True,
        required=False,
        label=mark_safe('Chromosome : Position ReferenceBase &gt; (AlternateBase|VariantType)'),
        label_suffix = '',
        error_messages = { 'required': "<p>Eh? ... What was the query again?</p>"},
        widget=forms.TextInput(attrs={'data-lpignore':'true', # data-lpignore=true to ignore LastPass injected code
                                      'placeholder': 'For example  10 : 12345 A > T'}),
    )
    

    includeDatasetResponses = forms.ChoiceField(required=True,
                                                choices=( (i.upper(),i) for i in ('All','Hit','Miss','None') ),
                                                label='Included Dataset Responses',
                                                widget=forms.Select,  # instead of IncludeDatasetResponsesWidget
                                                initial='ALL')
    
    print(includeDatasetResponses)
    def is_valid(self):
        self.full_clean() # Populate fields (or read self.errors)

        # Short circuit already 
        if not super().is_valid():
            return False

        query = self.cleaned_data.get('query')
        LOG.debug('Query: %s', query)

        # Since for this endpoint the query is not requiered
        if query:
            # So far so good
            self.query_deconstructed_data = None

            # Testing the regular Query
            m = regex.match(query)
            if m:
                d = { 'referenceName': m.group(1),
                    'start': m.group(2),
                    'referenceBases': m.group(3),
                    'includeDatasetResponses': self.cleaned_data.get('includeDatasetResponses'),
                    'assemblyId': self.cleaned_data.get('assemblyId') 
                }
                v = m.group(4)
                k = 'variantType' if v in variantTypes else 'alternateBases'
                d[k] = v
                self.query_deconstructed_data = d
                return True

            # Invalid query
            self.add_error('query', ValidationError(_('<p><span class="bold">Oops! </span>Query <code>%(value)s</code> must be of the form:</p>'
                                                    '<p><span class="query-form">Regular Query</span>Chromosome : Position ReferenceBase &gt; (AlternateBase|VariantType)</p>'
                                                    '<div class="small">'
                                                    '<p>where</p>'
                                                    '<ul>'
                                                    '<li>- Chromosome: 1-22, X, Y, or MT</li>'
                                                    '<li>- Position: a positive integer</li>'
                                                    '<li>- VariantType: either DEL:ME, INS:ME, DUP:TANDEM, DUP, DEL, INS, INV, CNV, SNP, or MNP</li>'
                                                    '<li>- ReferenceBase or AlternateBase: a combination of one or more A, T, C, G, or N</li>'
                                                    '</ul>'
                                                    '</div>'),
                                                    params={'value':query}))

            return False
        
        self.query_deconstructed_data = {   'includeDatasetResponses': self.cleaned_data.get('includeDatasetResponses'),
                                            'assemblyId': self.cleaned_data.get('assemblyId') 
                                        }
        return True
