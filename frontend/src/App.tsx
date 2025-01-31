import './App.css';
import { useDropzone } from 'react-dropzone';
import './Styles/styles.scss';

function App() {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    //accept: 'image/*',
    onDrop: (acceptedFiles) => {
      const file = acceptedFiles[0];
      console.log(file);
    }
  })

  return (
    <div {...getRootProps()} className="image-upload-box">
      <input {...getInputProps()} />
      {isDragActive ? 
        <p>Drop the files here...</p> :
        <p>Drag 'n' drop some files here, or click to select files</p>
      }
    </div>
  )
}

export default App
