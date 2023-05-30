import './GenomicVariations.css';
import '../App.css';

import LayoutIndividuals from './LayoutIndividuals';

function GenomicVariations(props) {


  return (
    <div>
    <LayoutIndividuals collection={'Variant'}  />
    <label>alternateBases</label>
    <input type='text'></input>
    <label>referenceBases</label>
    <input type='text'></input>
    <label>Start position</label>
    <input type='text'></input>
    <label>End position</label>
    <input type='text'></input>
    </div>
  )
}

export default GenomicVariations