# Build the React app
FROM node:20-alpine AS build
WORKDIR /app

# Copy only package.json first for better caching
COPY package.json ./

# npm ci requires package-lock.json; you don't have it, so use npm install
RUN npm install --no-audit --no-fund

# Copy the rest and build
COPY . .
RUN npm run build

# Serve using nginx
FROM nginx:alpine

# Copy built frontend
COPY --from=build /app/build /usr/share/nginx/html

# Replace nginx default config with our config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
