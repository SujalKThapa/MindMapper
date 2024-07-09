# MindMapper
A tool for generating pdf summaries as mindmaps. Live demo @ https://mindmapai.vercel.app/

# Demonstration Video
A video showcasing the application and the considerations to be taken into account when using the tool.


https://github.com/SujalKThapa/MindMapper/assets/136220535/3216ba4a-f457-4ce1-8b26-cdef61bbd454



# Technologies Used and Architecture

- Next.js
- Docker
- Azure Functions (Serverless) with Python
- OpenAI API
- Langchain
- Graphviz
  
The application architecture consists of a Next.js website hosted on a Vercel subdomain, which uses Azure's serverless functions to process PDFs and generate visual summaries/mindmaps. These mindmaps are then sent back to the website from the serverless function before finally being displayed to the user.


  ## Next.js and Vercel
  The website was built using Next.js, a React framework that supports Server-Side Rendering (SSR). The backend, implemented with Node.js, primarily involved sending HTTP requests with attached PDFs to a serverless function hosted on Azure and waiting for the response.
  The files for the website were then uploaded to the repository you are currently viewing, and then hosted on Vercel using its GitHub integration. 

  Also worth noting, Vercel's integration with the GitHub repository allows the replication of features typically reserved for a CI/CD pipeline, such as automatic deployments of pull requests.

  ## Docker
  The files for the serverless function were containerized using Docker before being uploaded to Docker Hub, this was done in order to streamline the process of installing the necessary dependencies and manage configurations, enabling the smooth operation of the function in the serverless environment.
