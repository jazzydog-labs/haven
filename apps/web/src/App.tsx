import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Records from "./pages/Records";
import DiffGeneration from "./pages/DiffGeneration";
import CommitViewer from "./components/diff/CommitViewer";

function App() {
  return (
    <Routes>
      <Route path="/diffs/commit/:commitHash" element={<CommitViewer />} />
      <Route path="/*" element={
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/records" element={<Records />} />
            <Route path="/diffs" element={<DiffGeneration />} />
          </Routes>
        </Layout>
      } />
    </Routes>
  );
}

export default App;
