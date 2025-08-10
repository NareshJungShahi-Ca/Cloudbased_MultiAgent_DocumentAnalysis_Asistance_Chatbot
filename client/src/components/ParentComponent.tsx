import { useState } from "react";
import InputPanel from "./InputPanel";
import OutputPanel from "./OutputPanel";

type UploadStatus = "idle" | "uploading" | "success" | "error";

const ParentComponent = () =>{
    // Shared State 
    const [result, setResult] = useState<string | null>(null);
    const [status, setStatus] = useState<UploadStatus>("idle");



return (
    <div>
        <OutputPanel result={result} status = {status}/>
        <InputPanel setResult = {setResult} setStatus = {setStatus}/>
    </div>
    );
};

export default ParentComponent