import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, FileText, CheckCircle, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import toast from "react-hot-toast";

const ResumeUpload = ({ onUploadSuccess, isLoading, setIsLoading }) => {
  const [resumeText, setResumeText] = useState("");
  const [uploadedFile, setUploadedFile] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;
    const allowedTypes = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    if (!allowedTypes.includes(file.type)) { toast.error("Please upload a PDF or DOCX file"); return; }
    if (file.size > 10 * 1024 * 1024) { toast.error("File size must be less than 10MB"); return; }
    setIsLoading(true); setUploadedFile(file);
    try {
      const formData = new FormData();
      formData.append("resume", file);
      const response = await fetch("/upload", { method: "POST", body: formData });
      const data = await response.json();
      if (data.status === "success") { toast.success("Resume processed! Found " + data.data.skills_found + " skills."); onUploadSuccess(data.data); }
      else { toast.error("Error processing resume: " + data.message); setUploadedFile(null); }
    } catch (error) { toast.error("Error uploading resume: " + error.message); setUploadedFile(null); }
    finally { setIsLoading(false); }
  }, [onUploadSuccess, setIsLoading]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"], "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] },
    multiple: false, disabled: isLoading,
  });

  const handleTextSubmit = () => {
    if (!resumeText.trim()) { toast.error("Please enter your resume text"); return; }
    onUploadSuccess({ resume_text: resumeText, text: resumeText, skills_found: 0, filename: "manual_input.txt" });
    toast.success("Resume text processed successfully!");
  };

  return (
    <div className="space-y-5">
      {/* Dropzone */}
      <div {...getRootProps()} className={"relative group cursor-pointer rounded-2xl border-2 border-dashed p-8 text-center transition-all duration-300 " +
        (isDragActive ? "border-blue-400 bg-blue-50 scale-[1.02]" :
         uploadedFile ? "border-emerald-400 bg-emerald-50" :
         "border-gray-200 hover:border-blue-400 hover:bg-blue-50/50") +
        (isLoading ? " opacity-60 cursor-not-allowed" : "")}>
        <input {...getInputProps()} />
        <AnimatePresence mode="wait">
          {isLoading ? (
            <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex flex-col items-center gap-3">
              <div className="relative w-14 h-14">
                <div className="absolute inset-0 rounded-full border-4 border-blue-100" />
                <div className="absolute inset-0 rounded-full border-4 border-blue-500 border-t-transparent animate-spin" />
              </div>
              <p className="font-semibold text-gray-700">Processing resume...</p>
            </motion.div>
          ) : uploadedFile ? (
            <motion.div key="success" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }} className="flex flex-col items-center gap-3">
              <div className="w-14 h-14 bg-emerald-100 rounded-2xl flex items-center justify-center">
                <CheckCircle className="w-8 h-8 text-emerald-600" />
              </div>
              <div>
                <p className="font-bold text-emerald-700 text-lg">File uploaded successfully!</p>
                <p className="text-sm text-gray-500 mt-0.5">{uploadedFile.name}</p>
              </div>
            </motion.div>
          ) : isDragActive ? (
            <motion.div key="drag" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex flex-col items-center gap-3">
              <div className="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center animate-bounce">
                <Upload className="w-8 h-8 text-blue-600" />
              </div>
              <p className="font-bold text-blue-700 text-lg">Drop it here!</p>
            </motion.div>
          ) : (
            <motion.div key="idle" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex flex-col items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-violet-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <Upload className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <p className="font-bold text-gray-800 text-base">Drop your resume here</p>
                <p className="text-sm text-gray-400 mt-1">or click to browse files</p>
              </div>
              <button type="button" className="btn-primary text-sm px-5 py-2">
                <FileText className="w-4 h-4" /> Choose File
              </button>
              <p className="text-xs text-gray-400">PDF and DOCX supported · Max 10MB</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Divider */}
      <div className="relative flex items-center gap-3">
        <div className="flex-1 h-px bg-gray-100" />
        <span className="text-xs text-gray-400 font-medium px-2">or paste resume text</span>
        <div className="flex-1 h-px bg-gray-100" />
      </div>

      {/* Text Input */}
      <div className="space-y-3">
        <textarea value={resumeText} onChange={e => setResumeText(e.target.value)}
          placeholder="Paste your resume content here..."
          className="w-full h-36 px-4 py-3 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-400 outline-none resize-none transition-all placeholder-gray-400 bg-gray-50 focus:bg-white"
          disabled={isLoading || !!uploadedFile} />
        <button onClick={handleTextSubmit} disabled={!resumeText.trim() || isLoading || !!uploadedFile}
          className="btn-primary w-full">
          Process Resume Text
        </button>
      </div>

      {/* Info */}
      <div className="flex items-start gap-3 p-4 bg-gradient-to-r from-blue-50 to-violet-50 border border-blue-100 rounded-xl">
        <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
          <Sparkles className="w-4 h-4 text-blue-600" />
        </div>
        <div>
          <p className="text-sm font-semibold text-gray-800">Smart Analysis</p>
          <p className="text-xs text-gray-500 mt-0.5">Our system uses advanced technology for comprehensive analysis and contextual skill matching.</p>
        </div>
      </div>
    </div>
  );
};

export default ResumeUpload;