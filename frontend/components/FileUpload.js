import { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Progress } from "./ui/progress";
import { Card, CardContent } from "./ui/card";
import { UploadCloud } from "lucide-react";
import axios from "axios";

export default function FileUpload() {
    const [file, setFile] = useState(null);
    const [progress, setProgress] = useState(0);
    const [message, setMessage] = useState("");

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
        setMessage("");
        setProgress(0);
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage("Selecione um arquivo primeiro!");
            return;
        }
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post(`${process.env.API_URL}/upload/`, formData, {
                headers: { "Content-Type": "multipart/form-data" },
                onUploadProgress: (progressEvent) => {
                    const percentComplete = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setProgress(percentComplete);
                }
            });
            setMessage(response.data.message);
        } catch (error) {
            setMessage("Erro ao enviar arquivo!");
        }
    };
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
            <Card className="p-6 w-96 shadow-lg">
                <CardContent className="flex flex-col items-center gap-4">
                   <h2 className="text-xl font-semibold">Upload de arquivo</h2>
                   <Input type="file" accept="audio/*, video/*" onChange={handleFileChange}/>
                    <Button onClick={handleUpload} className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600">
                        <UploadCloud size={18} />
                        Enviar arquivo
                    </Button>
                    {progress > 0 && <Progress value={progress} className="w-full" />}
                    {message && <p className="text-sm text-gray-700 mt-2">{message}</p>}
                </CardContent>
            </Card>
        </div>
    );
}
