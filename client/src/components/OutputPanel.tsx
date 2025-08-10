
type UploadStatus = "idle" | "uploading" | "success" | "error";
type OutputPanelProps = {
    result: string | null;
    status: UploadStatus
}
const OutputPanel = ({result, status}: OutputPanelProps) => {
    return (
        <>
        <div className="container">
            <h1>Hello, I am Document Analysis Assistance</h1>
        
        <div className="container mt-4 p-2 border border-gray-300">
            <h3>Output:</h3>
            {status === "uploading" && <p>Processing...</p>}
            {status === "error" && <p style={{ color: "red" }}>Error occurred. Please try again.</p>}
            {status === "success" && result && <p style={{ whiteSpace: "normal", wordWrap: "break-word" }}>{result}</p>}
            {status === "success" && !result && <p>No output received.</p>}
        </div>
        </div>
        </>
    );
}

export default OutputPanel

