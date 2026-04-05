# Deployment Guide

To deploy this demo for the hackathon (so it can be accessed on the internet rather than just `localhost`), you have two main approaches: **Cloud Platforms (Free Tier)** or **Docker (VPS)**.

## Approach 1: Deploy on Docker (Recommended if you have a VPS like DigitalOcean, AWS, or Azure)

We have already generated a `docker-compose.yml` and `Dockerfile` for all 3 components.

1. SSH into your server.
2. Clone your repository.
3. In `docker-compose.yml`, change `your-production-server-ip` to the actual IP address or domain name of your server.
4. Run the following command:
   ```bash
   docker-compose up --build -d
   ```
5. Your apps will be accessible on:
   - Manufacturer Dashboard: `http://<SERVER_IP>:5173`
   - Vehicle Emulator: `http://<SERVER_IP>:5174`
   - Backend API: `http://<SERVER_IP>:3000`

---

## Approach 2: Deploy on Vercel & Render (Easiest & Free)

If you don't have a virtual server, you can deploy the frontends to Vercel and the backend to Render.com.

### 1. Deploy the Backend (Render)
1. Push this code to GitHub.
2. Go to **Render.com** > New Web Service.
3. Connect your repository.
4. Set the Root Directory to `backend/`
5. Build Command: `npm install`
6. Start Command: `node server.js`
7. Once deployed, Render will give you a URL like `https://antigravity-backend.onrender.com`.

### 2. Deploy Frontends (Vercel)
1. Go to **Vercel.com** > Import Project.
2. Import the root repository.
3. When configuring, set the **Framework Preset** to Vite.
4. Set the **Root Directory** to `manufacturer-client/`.
5. Under Environment Variables, add:
   - Key: `VITE_API_URL`
   - Value: `https://antigravity-backend.onrender.com` (Your Render deployment URL)
6. Click Deploy!
7. Repeat the exact same steps for the `vehicle-client/` folder.
