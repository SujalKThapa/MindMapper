import Head from 'next/head';
import { useState, useEffect } from 'react';
import styles from '../styles/Home.module.css';

const handleButtonClick = () => {
  console.log("Button clicked");
  document.getElementById('pdfUpload').click();
};

const handleFileChange = async (event, showResult, imageHtml) => {
  console.log('File input changed');
  const file = event.target.files[0];
  if (file && file.type === 'application/pdf') {
    console.log('PDF file selected: ', file);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', 'Sujal');

    try {
      const response = await fetch('https://mindmapconverter.agreeablesmoke-94d8f4cf.eastus.azurecontainerapps.io/api/http_trigger?code=Vah2HQvHTNBucLKepYzKtRicsFYQagyq4H4f6eWoxAnpAzFunKTPtQ%3D%3D', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        console.log('File uploaded successfully: ', result);
        if (result.image_html && result.image_html !== imageHtml) {
          showResult(result.image_html);
        }
      } else {
        console.error('Error uploading file: ', response.statusText);
      }
    } catch (error) {
      console.error('Error uploading file: ', error);
    }
  } else {
    alert('Please select a PDF file');
  }
};

export default function Home() {
  const [imageHtml, setImageHtml] = useState('');
  const [isResultVisible, setIsResultVisible] = useState(false);

  const showResult = (html) => {
    console.log("Setting result HTML");
    setImageHtml(html);
    setIsResultVisible(true);
  };

  // Added useEffect to prevent infinite re-renders
  useEffect(() => {
    console.log("Home component mounted");
    return () => {
      console.log("Home component unmounted");
    };
  }, []);

  console.log("Rendering Home Component");
  console.log("isResultVisible:", isResultVisible);
  console.log("imageHtml:", imageHtml);

  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className={styles.header}>
        <a href="https://github.com/your-repo" target="_blank" rel="noopener noreferrer">
          <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" className={styles.githubIcon} alt="GitHub Repo" />
        </a>
      </header>

      <main className={styles.main}>
        <div className={styles.content}>
          <div className={styles.textBlock}>
            <div className={styles.mainTitle}>
              Mind Mapper
            </div>
            <h2 className={styles.subTitle}>
              Convert PDFs into Mind Maps
            </h2>
            <h3 className={styles.subTitle2}>
              Seamless summarization and transformation<br/>of your personal, educational and business<br/>documents into easy-to-digest Mind Maps.
            </h3>
            <button className={styles.uploadButton} onClick={handleButtonClick}>Upload PDF</button>
            <input
              type='file'
              id='pdfUpload'
              accept='application/pdf'
              style={{display:'none'}}
              onChange={(event) => handleFileChange(event, showResult, imageHtml)}
            />
          </div>
          <img src='https://i.postimg.cc/TPy6QKBp/Pdf2-Mind-Map.png' className={styles.image}/>
        </div>
      </main>

      {isResultVisible && (
        <div className={styles.resultBlock}>
          <h3>Result:</h3>
          {imageHtml && <div className={styles.innerImg} dangerouslySetInnerHTML={{ __html: imageHtml }} />}
          <button className={styles.anotherButton}>Another Action</button>
        </div>
      )}
      
      <style jsx global>{`
        html,
        body {
          padding: 0;
          margin: 0;
          font-family:
            -apple-system,
            BlinkMacSystemFont,
            Segoe UI,
            Roboto,
            Oxygen,
            Ubuntu,
            Cantarell,
            Fira Sans,
            Droid Sans,
            Helvetica Neue,
            sans-serif;
        }
        * {
          box-sizing: border-box;
        }
      `}</style>
    </div>
  );
}
