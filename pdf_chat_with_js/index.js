import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";
import { CharacterTextSplitter } from "@langchain/textsplitters";
import { OpenAIEmbeddings } from "@langchain/openai";
import { QdrantVectorStore } from "@langchain/qdrant";

const pdfPath = './nodejs.pdf';
const loader = new PDFLoader(pdfPath);

const textSplitter = new CharacterTextSplitter({
    chunkSize: 1000,
    chunkOverlap: 200,
});
const texts = await textSplitter.splitText(loader)

const embedder = new OpenAIEmbeddings(
    {
        model: "text-embedding-3-large",
        api_key: process.env.OPENAI_API_KEY
    }
)


const vector_store = new QdrantVectorStore.fromDocuments({
    url: "http://localhost:6333",
    collectionName: "pdf_chat_js",
    embedding: embedder
})


const injection = await vectorStore.addDocuments(documents); 

console.log(texts);


