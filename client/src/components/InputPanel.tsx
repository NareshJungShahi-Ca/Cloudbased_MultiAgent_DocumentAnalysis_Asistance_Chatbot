import { useState, type ChangeEvent } from "react";
import axios  from 'axios';
type UploadStatus = "idle" | "uploading" | "success" | "error";

type InputPanelProps = {
  setResult: React.Dispatch<React.SetStateAction<string | null>>;
  setStatus: React.Dispatch<React.SetStateAction<UploadStatus>>;
};

type ProcessResponse = {
  status: string;
  result: string;
};

const InputPanel = ({ setResult, setStatus }: InputPanelProps) => {
    const [fileName, setFilename] = useState<File | null>(null);
    const [prompt, setPrompt] = useState(''); 
    // const [status, setStatus] = useState<UploadStatus>("idle");

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) =>{
        if (e.target.files){
            setFilename(e.target.files[0]);
            setResult(null);
            setStatus("idle");
        }
    } 

    const handlePromptChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
            setPrompt(e.target.value);
            setResult(null);
            setStatus("idle");
    }

    const handleFileupload = async () => {
        if (!fileName && !prompt) return alert("please enter a prompt or upload a file!");
        setStatus("uploading");
        const formData = new FormData();
        // formData.append("file", fileName!)
        // formData.append("prompt", prompt)
        if (fileName) formData.append("file", fileName);
        if (prompt.trim()) formData.append("prompt", prompt.trim());

        try{
            const response = await axios.post<ProcessResponse>( "http://127.0.0.1:8000/process/", formData, {
                headers:{
                    "Content-type": "multipart/form-data"
                },
            });
            // setResult(response.data.result || "No result returned");
            // response.data.result might be an object with nested summary
            const backendResult = response.data.result as any;
            if (backendResult && typeof backendResult === "object" && backendResult.result) {
                setResult(backendResult.result); // pass summary string to OutputPanel
                } else if (typeof backendResult === "string") {
                    setResult(backendResult);
                } else {
                    setResult("No result returned");
                }

            setStatus("success")

        } catch(error) {
            console.error("Error in file upload:", error);
            setResult(null);
            setStatus("error"); 
        }

    }
  

    return (
        <>
        <div className='container h-96 p-4 gap-4'>
                <textarea className="w-1/2 h-full border p-2 rounded resize-none"
                    placeholder="Enter prompt here..."
                    value={prompt}
                    onChange={handlePromptChange}
                />
            

                <div className="flex flex-col justify-start gap-2 w-1/2">
                <input type = 'file' onChange={handleFileChange}/><br/>
                {(fileName || prompt) && status !== 'uploading' && <button onClick={handleFileupload}>Ask</button>}
                </div>
            </div>
        </>
    );
};


export default InputPanel