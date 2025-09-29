# Tax Education Agent 🇵🇰

This project is an AI-powered **Tax Assistant Agent** designed to help startups, freelancers, and entrepreneurs in Pakistan understand the basics of taxation and compliance.

## 📚 Data Sources
The agent has been enriched with knowledge extracted and embedded into **Pinecone Vector Database** from the following trusted resources:

- [FBR – Income Tax Basics](https://fbr.gov.pk/income-tax-basics/51147/61148)  
- [Startup.pk – PSEB Registration Made Easy (2025)](https://www.startup.pk/pseb-registration-made-easy-what-every-startup-founder-needs-to-know-in-2025/)  
- [Startup.pk – Handling Taxes as a Startup/Freelancer (2025)](https://www.startup.pk/how-to-handle-taxes-in-pakistan-as-a-startup-and-freelancer-2025/)  

More cominwill ne integrated soon..

## 🚀 Purpose
- To **educate startups** about taxation and registration processes in Pakistan.  
- To **assist freelancers** in understanding their tax responsibilities.  
- To **increase knowledge among Pakistani entrepreneurs** so they can make informed financial and business decisions.  

## ⚙️ How It Works
1. Web content is **scraped and cleaned**.  
2. Text is **chunked and converted into embeddings** using OpenAI.  
3. Embeddings are stored in **Pinecone** for semantic search.  
4. The AI agent retrieves relevant chunks and provides **context-aware answers**.  
5. Users can ask questions in **English or Urdu**, and the agent adapts accordingly.  

## 🌍 Vision
By combining **AI + local tax knowledge**, this project aims to make Pakistan’s taxation system easier to understand for **founders, freelancers, and small businesses**.

## 🔮 Future Resources
In the future, this project can expand into a **multi-agent ecosystem** where different specialized LLMs (Large Language Models) handle unique categories of users and tasks. For example:

- **Freelancers Agent** → Focused on freelance taxation and registration.  
- **Business Owners Agent** → Covers company compliance, tax filings, and business structures.  
- **Startups Agent** → Assists early-stage startups with PSEB registration, NTN, and compliance.  
- **Tech Startups Agent** → Special focus on IT/export-related tax benefits.  
- **Entrepreneurs Agent** → General guidance on scaling, compliance, and financial awareness.  

Using **handoff agent tasks**, conversations can smoothly transfer between these specialized agents, giving users **expert-level answers tailored to their situation**.
