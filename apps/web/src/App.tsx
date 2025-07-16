import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Records from "./pages/Records";
import DiffGeneration from "./pages/DiffGeneration";

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/records" element={<Records />} />
        <Route path="/diffs" element={<DiffGeneration />} />
      </Routes>
    </Layout>
  );
}

export default App;
