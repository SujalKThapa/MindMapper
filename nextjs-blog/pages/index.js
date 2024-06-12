import Head from 'next/head';
import styles from '../styles/Home.module.css';

export default function Home() {
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
            <button className={styles.uploadButton}>Upload PDF</button>
          </div>
          <img src='https://i.postimg.cc/TPy6QKBp/Pdf2-Mind-Map.png' className={styles.image}/>
        </div>
      </main>
      
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
