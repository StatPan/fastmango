# Guide: Deploying Your Application

This guide will walk you through the process of deploying your FastMango application to various hosting platforms.

## Overview

FastMango is designed to be easy to deploy to a variety of modern hosting platforms. Our goal is to provide a "one-click" deployment experience with the `fastmango deploy` command, but we're not there yet.

In the meantime, this guide will show you how to manually deploy your application to some of the most popular PaaS (Platform-as-a-Service) providers.

## Preparing Your Application for Deployment

Before you can deploy your application, you need to make a few changes to your code to get it ready for a production environment.

### 1. Configure Your Database

In development, you're likely using a simple SQLite database. For production, you'll want to use a more robust database like PostgreSQL.

You'll need to update the `database_url` in your `MangoApp` instance to point to your production database. It's recommended to use an environment variable for this, so you don't have to hardcode your database credentials in your code.

```python
import os
from fastmango import MangoApp

app = MangoApp(
    database_url=os.getenv("DATABASE_URL"),
)
```

### 2. Create a `requirements.txt` File

Most PaaS providers will need a `requirements.txt` file to know which Python packages to install.

While you can use `pip freeze > requirements.txt` to generate this file, we recommend using [uv](https://github.com/astral-sh/uv), a next-generation package manager that is significantly faster than `pip`.

To create a `requirements.txt` file with `uv`, run:

```bash
uv pip freeze > requirements.txt
```

### 3. Configure Your `Procfile`

A `Procfile` is a file that tells the hosting platform how to run your application. For a FastMango application, your `Procfile` should look like this:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

This command tells the platform to run your application using the `uvicorn` server, and to listen on the host and port specified by the platform.

## Deploying to PaaS Providers

Here are some general instructions for deploying to popular PaaS providers. For more detailed instructions, please refer to the documentation for the specific platform you're using.

### Railway

Railway is a modern PaaS that makes it easy to deploy applications. To deploy your FastMango application to Railway:

1.  Create a new project on Railway and connect it to your GitHub repository.
2.  Add a PostgreSQL database to your project. Railway will automatically set the `DATABASE_URL` environment variable for you.
3.  Railway will automatically detect your `Procfile` and `requirements.txt` file and deploy your application.

### Fly.io

Fly.io is a platform for deploying applications in Docker containers to a global network of servers. To deploy your FastMango application to Fly.io:

1.  Install the `flyctl` command-line tool and log in to your Fly.io account.
2.  Run `fly launch` in your project directory. This will automatically detect your application and generate a `fly.toml` configuration file.
3.  Run `fly deploy` to deploy your application.

### Render

Render is another popular PaaS that makes it easy to deploy applications. To deploy your FastMango application to Render:

1.  Create a new "Web Service" on Render and connect it to your GitHub repository.
2.  Set the "Start Command" to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
3.  Add a PostgreSQL database to your project and set the `DATABASE_URL` environment variable in your web service.
4.  Render will automatically deploy your application whenever you push changes to your GitHub repository.

## Future Plans

In the future, we plan to provide a more streamlined deployment experience with the `fastmango deploy` command. This will allow you to deploy your application to various platforms with a single command, without having to manually configure your application for each platform.

We also plan to provide built-in support for containerization with Docker and deployment to major cloud providers like AWS, Google Cloud, and Azure. Stay tuned for updates!


## 🚀 Deployment

### One-Click Deployment
fastmango는 **개발부터 배포까지 완전한 개발자 경험**을 제공합니다.

```bash
# 프로덕션 배포
fastmango deploy railway
fastmango deploy fly.io
fastmango deploy render
```

### 지원하는 플랫폼
- Railway.app
- Fly.io  
- Render.com
- AWS/GCP/Azure

### 데이터베이스
- PostgreSQL 중심 아키텍처
- 자동 스케일링 지원
- 백업 및 복구 기능
