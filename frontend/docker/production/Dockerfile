FROM node:20-alpine

# Set working directory to /app
WORKDIR /frontend

# Copy package*.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Run command
CMD ["npm", "start"]

