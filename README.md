# Grid Image Generator

A web application that adds customizable grid overlays to PNG images. Built with Vite, React, TypeScript, and Python.

## Features

- Upload PNG images
- Customize grid line width (1-10px)
- Customize grid line spacing (5-100px)
- Live preview of original and processed images
- Download processed images
- Serverless Python backend using Vercel Functions

## Project Structure

```
grid-upload/
├── api/
│   └── grid.py              # Vercel serverless function
├── src/
│   ├── App.tsx              # Main React component
│   ├── App.css              # Styling
│   └── main.tsx             # Entry point
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
└── README.md
```

## Local Development

### Prerequisites

- Node.js (v18 or higher)
- Python 3.9+
- npm or yarn

### Installation

1. Install Node.js dependencies:
```bash
npm install
```

2. Install Python dependencies (optional for local testing):
```bash
pip install -r requirements.txt
```

### Running Locally

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

**Note:** The Python API function won't work locally without Vercel CLI. To test the full functionality locally:

```bash
npm install -g vercel
vercel dev
```

## Deployment to Vercel

### Option 1: Deploy via Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel
```

4. For production deployment:
```bash
vercel --prod
```

### Option 2: Deploy via Vercel Dashboard

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)

2. Go to [vercel.com](https://vercel.com) and sign in

3. Click "New Project"

4. Import your repository

5. Vercel will automatically detect the configuration from `vercel.json`

6. Click "Deploy"

### Environment Configuration

The application works out of the box without any environment variables. Vercel automatically:
- Builds the frontend with `npm run build`
- Deploys the `dist` folder as static files
- Configures the `/api/grid` endpoint as a Python serverless function
- Installs Python dependencies from `requirements.txt`

## How It Works

### Frontend (React + TypeScript)

- Built with Vite for fast development and optimized production builds
- Form to upload PNG images and configure grid parameters
- Sends multipart form data to the `/api/grid` endpoint
- Displays original and processed images side-by-side
- Provides download functionality for the processed image

### Backend (Python Serverless Function)

- Located in `api/grid.py`
- Handles POST requests with multipart form data
- Processes images in-memory using the `pypng` library
- Returns the processed image as a PNG response
- Automatically scales with Vercel's serverless infrastructure

### Grid Algorithm

The Python function draws grid lines on the image by:
1. Reading the PNG image data
2. Drawing horizontal lines at specified intervals
3. Drawing vertical lines at specified intervals
4. Setting grid pixels to black (RGB: 0,0,0) with full opacity
5. Supporting grayscale, RGB, and RGBA image formats

## Technologies Used

- **Frontend:** React, TypeScript, Vite
- **Backend:** Python 3.9, pypng
- **Hosting:** Vercel (Serverless Functions + Static Hosting)
- **Image Processing:** pypng library

## Limitations

- Only supports PNG image format
- Maximum file size depends on Vercel's serverless function limits (default 4.5MB request body)
- Processing time limited by Vercel's serverless function timeout (default 10 seconds)

## License

ISC
