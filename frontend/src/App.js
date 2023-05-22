import 'devextreme/dist/css/dx.light.css';

import './App.css';
import { Route, Routes } from 'react-router-dom';

import Individuals2 from './components/Individual2';
import GenomicVariations from './components/GenomicVariations';
import Biosamples from './components/Biosamples';
import Runs from './components/Runs';
import Analyses from './components/Analyses';
import Cohorts from './components/Cohorts';
import Datasets from './components/Datasets'
import ErrorPage from './pages/ErrorPage';
import Navbar from './components/Navbar';
import History from './components/History';
import SignInForm from './components/SignInForm';
import SignUpForm from './components/SignUpForm';
import ResultsDatasets from './components/ResultsDatasets';
import CrossQueries from './components/CrossQueries';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path='/' element={<Individuals2 />} />
        <Route path='/individuals' element={<Individuals2 />} />
        <Route path='/genomicVariations' element={<GenomicVariations />} />
        <Route path='/biosamples' element={<Biosamples />} />
        <Route path='/runs' element={<Runs />} />
        <Route path='/analyses' element={<Analyses />} />
        <Route path='/cohorts' element={<Cohorts />} />
        <Route path='/datasets' element={<Datasets />} />
        <Route path='/members' element={<ResultsDatasets />} />
        <Route path='/history' element={<History />} />
        <Route path='/sign-up' element={<SignUpForm />} />
        <Route path="/sign-in" element={<SignInForm />} />
        <Route path="/cross-queries" element={<CrossQueries />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </div>
  );
}



export default App;