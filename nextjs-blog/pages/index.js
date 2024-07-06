import Head from 'next/head';
import { useState, useEffect } from 'react';
import { PDFDocument } from 'pdf-lib';
import styles from '../styles/Home.module.css';
import Swal from 'sweetalert2';

const handleButtonClick = () => {
  console.log("Button clicked");
  document.getElementById('pdfUpload').click();
};

const handleFileChange = async (event, showResult, imageHtml, setLoading) => {
  console.log('File input changed');
  const file = event.target.files[0];
  if (file && file.type === 'application/pdf') {
    console.log('PDF file selected: ', file);

    // Check PDF properties
    const arrayBuffer = await file.arrayBuffer();
    const pdfDoc = await PDFDocument.load(arrayBuffer);
    const numberOfPages = pdfDoc.getPageCount();

    if (numberOfPages > 30) {
      Swal.fire('Please select a PDF file with 30 pages or less');
      return;
    }

    if (numberOfPages === 0) {
      Swal.fire('The selected PDF file has no pages');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', 'Sujal');

    setLoading(true);
    const timeoutId = setTimeout(() => {
      setLoading(false);
      Swal.fire('Loading is taking too long. Please try again later.');
    }, 30000);

    try {
      const response = await fetch('https://mindmapconverter.agreeablesmoke-94d8f4cf.eastus.azurecontainerapps.io/api/http_trigger?code=Vah2HQvHTNBucLKepYzKtRicsFYQagyq4H4f6eWoxAnpAzFunKTPtQ%3D%3D', {
        method: 'POST',
        body: formData
      });

      clearTimeout(timeoutId);

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
    } finally {
      setLoading(false); 
    }
  } else {
    Swal.fire('Please select a PDF file');
  }
};

export default function Home() {
  const [imageHtml, setImageHtml] = useState('');
  const [isResultVisible, setIsResultVisible] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const showResult = (html) => {
    console.log("Setting result HTML");
    setImageHtml(html);
    setIsResultVisible(true);
  };

  const downloadImage = () => {
    const link = document.createElement('a');
    link.href = extractImageUrl(imageHtml);
    link.download = 'mindmap.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const openImage = () => {
    const link = document.createElement('a');
    link.href = extractImageUrl(imageHtml);
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const extractImageUrl = (html) => {
    const div = document.createElement('div');
    div.innerHTML = html;
    const img = div.querySelector('img');
    return img ? img.src : '';
  };

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
        <title>AI Mind Mapper | PDF to Mind Map using Gemini AI</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <header className={styles.header2}>
      <img src="https://i.postimg.cc/bJ3sKc5B/images-2.png"/>
      Mind Mapper
      </header>
      <header className={styles.header}>
        <a href="https://github.com/SujalKThapa/MindMapper" target="_blank" rel="noopener noreferrer">
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
            </h3>{!isResultVisible && (
  <>
    <div className={styles.pdfSection}>
      <button className={styles.uploadButton} onClick={handleButtonClick}>
        Upload PDF
      </button>
      <input
        type='file'
        id='pdfUpload'
        accept='application/pdf'
        style={{ display: 'none' }}
        onChange={(event) => handleFileChange(event, showResult, imageHtml, setIsLoading)}
      />
      <div className={styles.tooltipContainer}>
        <div className={styles.questionMark}>?</div>
        <div className={styles.tooltipText}>
          <div className={styles.criteriaTitle}><b>Upload Criteria:</b></div>
          <ul className={styles.criteriaList}>
          <li>The PDF must have extractable text.</li>
          <li>PDFs larger than 30 pages are to be avoided.</li>
          </ul>
        </div>
      </div>
      {isLoading && <div className={styles.loadingCircle}></div>}
    </div>
  </>
)}

          </div>
          <img src='https://i.postimg.cc/TPy6QKBp/Pdf2-Mind-Map.png' className={styles.image}/>
        </div>
      </main>

      {isResultVisible && (
        <div className={styles.resultBlock}>
          <h3>Result:</h3>
          {imageHtml && <div className={styles.innerImg} dangerouslySetInnerHTML={{ __html: imageHtml }} />}
          <button className={styles.anotherButton} onClick={downloadImage}>Download Image</button>
        </div>
      )}
      
      <style jsx global>{`
        html,
        body {
          padding: 0;
          margin: 0;
          font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
        }
        * {
          box-sizing: border-box;
        }
      `}</style>
    </div>
  );
}
