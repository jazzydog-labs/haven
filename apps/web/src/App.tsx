import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Records from "./pages/Records";
import DiffGeneration from "./pages/DiffGeneration";
import Dashboards from "./pages/Dashboards";
import CommitViewer from "./components/diff/CommitViewer";
import { CommitReviewPage } from "./pages/CommitReview";
import { RepositoryBrowserPage } from "./pages/RepositoryBrowser";
import { RepositoriesPage } from "./pages/Repositories";

function App() {
  return (
    <Routes>
      <Route path="/diffs/commit/:commitHash" element={<CommitViewer />} />
      <Route path="/commits/:commitHash/review" element={<CommitReviewPage />} />
      <Route path="/repository/:repositoryHash/browse" element={<RepositoryBrowserPage />} />
      <Route
        path="/*"
        element={
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/records" element={<Records />} />
              <Route path="/repositories" element={<RepositoriesPage />} />
              <Route path="/diffs" element={<DiffGeneration />} />
              <Route path="/dashboards" element={<Dashboards />} />
            </Routes>
          </Layout>
        }
      />
    </Routes>
  );
}

export default App;
