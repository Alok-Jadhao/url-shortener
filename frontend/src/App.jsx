import { useState } from "react";
import api from "./api";

function App() {
    const [url, setUrl] = useState("");
    const [history, setHistory] = useState([]);
    const [error, setError] = useState("");

    const shorten = async () => {
        try {
            setError("");
            const res = await api.post("/shorten", {
                original_url: url
            });

            setHistory([res.data, ...history]);
            setUrl("");
        } catch (err) {
            setError("Failed to shorten URL");
        }
    }


    return (
        <div style={{padding: "40px", fontFamily: "sans-serif"}}>
            <h2>Url Shortener</h2>

            <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter long URL"
            style={{width: "300px", padding: "8px"}}
            />

            <button onClick={shorten} style={{marginLeft: "10px"}}>
                Shorten
            </button>

            {error && <p style={{color: "red"}}>{error}</p>}

            <h3>History</h3>
            <ul>
                {history.map((item, index) => (
                    <li key={index}>
                        <a href={item.shorten_url} target="_blank">
                            {item.shorten_url}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default App;

