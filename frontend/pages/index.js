import FileUpload from "../components/FileUpload";

export default function Home() {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
          <FileUpload />
      </div>
    );
}