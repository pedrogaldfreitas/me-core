import './App.css';
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import './Styles/styles.scss';

function App() {
  const [imgChosen, setImgChosen] = useState('');

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    //accept: 'image/*',
    onDrop: (acceptedFiles) => {
      const file: File = acceptedFiles[0];
      const endpoint: string = 'http://localhost:8000/image';
      const formData: FormData = new FormData();

      formData.append('file_upload', file);

      try {
        fetch(endpoint, {
          method: "POST",
          body: formData
        }).then(res=>console.log(res))//.then(res => res.json()).then((data) => console.log(data.message.message.content)/*data => setImgChosen(data.message)*/);
      } catch (e) {
        console.log("Error | " + e);
      }
      console.log(file);
    }
  })

  return (
    <div {...getRootProps()} className="image-upload-box">
      {imgChosen}
      <input {...getInputProps()} />
      {isDragActive ? 
        <p>Drop the files here...</p> :
        <p>Drag 'n' drop some files here, or click to select files</p>
      }
    </div>
  )
}

export default App
