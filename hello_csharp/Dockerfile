# syntax=docker/dockerfile:1

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS builder

WORKDIR /src
COPY hello_csharp.csproj ./
RUN dotnet restore
COPY Program.cs ./
RUN dotnet publish -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0

RUN useradd -r -m -d /app appuser

WORKDIR /app

COPY --from=builder /app/publish ./

RUN mkdir -p /app/events \
    && chown -R appuser:appuser /app

ENV APP_HOST=0.0.0.0
ENV PORT=3005

EXPOSE 3005

USER appuser

CMD ["dotnet", "hello_csharp.dll"]
