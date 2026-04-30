# Design Tradeoffs

## Simple Scripts vs Full Application Framework

This repo uses small Python modules instead of Flask, Django, Airflow, or a frontend framework.

Reason: the project goal is to demonstrate API integration, data transformation, reporting, and testability without unnecessary infrastructure.

## CSV Outputs vs Database

The pipeline writes CSV files instead of using a database.

Reason: CSV keeps the outputs easy to inspect and simple to explain. A database would make sense if the project needed historical trends, multiple users, or scheduled long-term storage.

## Static HTML vs Web App

The dashboard is a static HTML file.

Reason: it can be opened directly in a browser and does not require a server. This is enough for a portfolio demo and mirrors many internal engineering reports.

## Live API Scripts vs Fully Mocked Demo

The export scripts call real Jira and GitHub APIs, while tests focus on pure local logic.

Reason: the project demonstrates real integration while keeping tests reliable and independent of credentials or network access.

