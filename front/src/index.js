import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter as Router, Route } from 'react-router-dom';
import ExplorePage from './pages/ExplorePage';
import ExplorePage1 from './pages/ExplorePage1';
import FeaturePage from './pages/FeaturePage';
import DashboardPage from './pages/DashboardPage';
import InputPage from './pages/InputPage';
import App from './App';
ReactDOM.render(
  <Router>
    <App>
      <Route key="index" exact path="/" component={DashboardPage} />
      <Route key="input" exact path="/input" component={InputPage} />
      <Route key="explore" path="/explore" component={ExplorePage} />
      <Route key="explore1" path="/explore1" component={ExplorePage1} />
      <Route key="feature" path="/feature" component={FeaturePage} />
    </App>
  </Router>, // eslint-disable-next-line no-undef
  document.getElementById('root')
);
