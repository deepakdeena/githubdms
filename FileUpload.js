import React, { useState, useEffect } from 'react';
import axios from 'axios';

function FileUpload() {
    const [file, setFile] = useState(null);
    const [images, setImages] = useState([]);

    useEffect(() => {
        fetchAllImages(); // Fetch images on component mount
    }, []);

    const fetchAllImages = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:5000/get_all_images");
            setImages(response.data.images);  // Store retrieved image URLs
        } catch (error) {
            console.error("Error fetching images:", error);
        }
    };

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please select a file first.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            await axios.post("http://127.0.0.1:5000/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });

            fetchAllImages();  // Refresh image list after upload
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    return (
        <div>
            <h1>PDF Image Extractor</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>

            <div>
                {images.length > 0 && <h2>Extracted Images:</h2>}
                {images.map((image, index) => (
                    <img 
                        key={index} 
                        src={`http://127.0.0.1:5000${image}`} 
                        alt={`Extracted ${index}`} 
                        style={{ width: "200px", margin: "10px" }} 
                    />
                ))}
            </div>
        </div>
    );
}

export default FileUpload;
