import { useEffect, useState } from "react";
import { getHealth, type HealthResponse } from "./services/api";

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const data = await getHealth();
        setHealth(data);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to connect to backend"
        );
      }
    };

    checkBackend();
  }, []);

  return (
    <main>
      <h1>AI Software Engineering Assistant</h1>

      <p>
        M.Tech Project using Retrieval-Augmented Generation
      </p>

      <hr />

      <h2>System Status</h2>

      {health && (
        <div>
          <p>
            Backend: <strong>{health.status}</strong>
          </p>

          <p>Service: {health.service}</p>

          <p>API Version: {health.version}</p>
        </div>
      )}

      {error && (
        <p>
          Backend connection failed: {error}
        </p>
      )}
    </main>
  );
}

export default App;