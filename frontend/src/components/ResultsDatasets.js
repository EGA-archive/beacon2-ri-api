
import './ResultsDatasets.css'

function ResultsDatasets() {

    return (
        <div className='resultsRecord'>
            <h3>CINECA SYNTHETIC COHORT DATASETS</h3>

            <div className="datasetsContainer">

                <div className="datasetCard">
                    <div className='tittle'>
                        <h1>Beacon Africa</h1>
                    </div>
                    <hr className='line'></hr>
                    <p>This dataset consists of 100 samples which have synthetic subject attributes and phenotypic data based on the Human Heredity and Health in Africa (H3Africa) consortium core phenotype model (H3Africa Core phenotype). The H3Africa initiative consists of 51 African projects, with over 70,000 participants, including population-based genomic studies of common, non-communicable disorders such as heart and renal disease, as well as communicable diseases such as tuberculosis.
                    </p>
                    <a href="#">Beacon API</a>
                    <a href="#">Visit us</a>
                    <a href="#">Contact us</a>
                </div>
                <div className="datasetCard">
                    <div className='tittle'>
                        <h1>Beacon Canada</h1>
                    </div>
                    <hr className='line'></hr>
                    <p>This dataset consists of 100 variables for 150 synthetic participants which have subject attributes and phenotypic data derived from the CHILD Cohort Study and the associated CHILDdb database. CHILD is a longitudinal study following over 3400 Canadian children and their parents, reflective of Canadian demographics, in order to better predict, prevent and treat chronic diseases. Variables were chosen from CHILDdb which covered the CINECA minimal metadata model, covered select COVID-specific and CINECA use cases and exhibited particular variables that are reflective of the CHILD Cohort Study. Note that there are over 37 million datapoints in CHILDdb, so this synthetic data is a very small subset of the very diverse, deeply phenotyped CHILD data.</p>
                    <a href="#">Beacon API</a>
                    <a href="#">Visit us</a>
                    <a href="#">Contact us</a>
                </div>
                <div className="datasetCard">
                    <div className='tittle'>
                        <h1>Beacon Europe UK1</h1>
                    </div>
                    <hr className='line'></hr>
                    <p>This dataset consists of 2504 samples which have genetic data based on 1000 Genomes data (phase3 and Geuvadis), and 76 synthetic subject attributes and phenotypic data derived from UKBiobank. The UK Biobank is a very large and detailed prospective study with over 500,000 participants aged 40–69 years when recruited in 2006–2010. The study has collected and continues to collect extensive phenotypic and genotypic detail about its participants, including data from questionnaires, physical measures, sample assays, accelerometry, multimodal imaging, genome-wide genotyping and longitudinal follow-up for a wide range of health-related outcomes.
                    </p>
                    <a href="#">Beacon API</a>
                    <a href="#">Visit us</a>
                    <a href="#">Contact us</a>
                </div>
                <div className="datasetCard">
                    <div className='tittle'>
                        <h1>Beacon Europe CH SIB</h1>
                    </div>
                    <hr className='line'></hr>
                    <p>This dataset consists of 6733 synthetic samples containing both phenotypic and genotypic information. The phenotypic data were derived from CoLaus and PsyCoLaus, cohorts which include data from over 6000 Caucasian individuals aged 35 to 75 years living in Lausanne, Switzerland. Although CoLaus focuses on cardiovascular disorders, and PsyCoLaus focuses on psychiatric disorders, both cohorts collect demographic, socio-economic, life-style, and clinical information from enrolled patients.</p>
                    <a href="#">Beacon API</a>
                    <a href="#">Visit us</a>
                    <a href="#">Contact us</a>
                </div>
            </div>
        </div>

    )

}

export default ResultsDatasets;