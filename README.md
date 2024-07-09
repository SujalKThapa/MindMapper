# MindMapper
A tool for generating pdf summaries as mindmaps. Live demo @ https://mindmapai.vercel.app/
 <br/> <br/>
# Demonstration Video
A video showcasing the application and the considerations to be taken into account when using the tool. <br/>
**[Note: The latest version of the application has shifted to using Google's Gemini models rather than OpenAI's GPT models]**


https://github.com/SujalKThapa/MindMapper/assets/136220535/3216ba4a-f457-4ce1-8b26-cdef61bbd454


<br/>

# Technologies Used and Architecture

- Next.js
- Azure functions
- Python
- Docker
- OpenAI API **[Now replaced with Google's Gemini]**
- Langchain

  
The application architecture consists of a Next.js website hosted on a Vercel subdomain, which uses Azure's serverless functions to process PDFs and generate visual summaries/mindmaps. These mindmaps are then sent back to the website from the serverless function before finally being displayed to the user.
<br/>
<br/>

  ## Next.js and Vercel
  The website was built using Next.js, a React framework that supports Server-Side Rendering (SSR). The backend, implemented with Node.js, primarily involved sending HTTP requests with attached PDFs to a serverless function hosted on Azure and waiting for the response.
  The files for the website were then uploaded to the repository you are currently viewing, and then hosted on Vercel using its GitHub integration. 

  Also worth noting, Vercel's integration with the GitHub repository allows the replication of features typically reserved for a CI/CD pipeline, such as automatic deployments of pull requests.
 <br/> 
<br/>
 
  ## Python (w/Graphviz)
  A Python function that takes a PDF document as input and returns an encoded image of the mindmap powers the serverless function, and works in three simple steps: 
  
  1) Extracting the text from PDF
  2) Sending the text content alongside a custom prompt to an OpenAI API **[Now replaced by Gemini]** 
  3) Turning the structured response from the API into a diagram using the Graphviz python library.
<br/>

  ## Docker
  The files for said Python function were then containerized using Docker before being uploaded to Docker Hub, this was done in order to streamline the process of installing the necessary dependencies and manage configurations, enabling the smooth operation of the function in the serverless environment.
 <br/>
<br/>

 ## Azure functions
 Azure Functions is an example of "Functions as a Service" (FaaS). In this computing model, a function is a piece of code deployed to the cloud—in this case, Microsoft Azure. This allows developers to run event-driven code without having to allocate or manage infrastructure.

The primary reasons for using Azure Functions for this project were twofold:

1) Cost-effectiveness: Unlike with other compute services, such as Azure Virtual Machines, which require 24/7 operational costs, Azure Functions bills the developer only for the function calls and the execution time. This makes it ideal for this project, where compute services are needed only when PDFs are uploaded, and not around the clock.

2) Scalability and Convenience: Since Azure functions are a managed service, meaning that Azure, not us, handles the allocation of resources and isolation of function instances from one another thus making them highly scalable. It is also easy to set-up and convenient to both use and maintain.
<br/>

## Gemini API
A request is sent to Gemini with the text content of the PDF prefixed by the following custom prompt:

```
Generate a title for this data, classify the data into sections as you see fit (and if the subject matter is really complex, into sub-sections) with summaries for the bottom level section/subsection. (Note: Try to maximize the number of sub-sections when summarizing while keeping the number of sections at a minimum.)
MUST FOLLOW THE FORMAT OF THE FOLLOWING EXAMPLE:
## Title: <Title>\n**Section: <Section Name>**\n Summary: <Section Summary>.\n**Section: <Section Name>**\nSummary: <Section Summary>\n**Sub-Section: <Subsection Name>**\nSummary: <Subsection Summary> \n**Sub-Section: <Subsection Name>**\nSummary: <Subsection Summary> \n**Section: <Section Name>**\nSummary: <Section Summary>\n
```
<br/>
The response, which is intended to be genereated in the specified format is then passed through a piece of python code that uses graphviz to generate an image where the title is the root node with the sections as the child nodes. 
<br/><br/>
If the subject matter of a section child node is complex enough to warrant sub-sections, then the same piece of code will also turn the sub-sections into child nodes, with the section node as their parents. As shown in the demo video.

<br/> <br/>

# Author's Note
Though originally created simply as a personal project to put on my CV/Resume, I later decided to spend a little extra time to turn the project into an actual tool and release it on ProductHunt for public use. So if you found the tool useful, please do follow the project on ProductHunt.

<a href="https://www.producthunt.com/products/mind-mapper/reviews?utm_source=badge-product_review&utm_medium=badge&utm_souce=badge-mind&#0045;mapper" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/product_review.svg?product_id=588623&theme=light" alt="Mind&#0032;Mapper - Summarize&#0032;PDF&#0032;documents&#0032;into&#0032;Concise&#0044;&#0032;digestible&#0032;Mind&#0032;Maps&#0046; | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a> 
