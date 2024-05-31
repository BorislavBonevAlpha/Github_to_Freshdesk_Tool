# GitHub to Freshdesk Contact Sync Tool

This Python program retrieves user information from **GitHub** and creates a new contact, updates it with an existing contact or deletes in **Freshdesk**.

## Introduction

This tool automates the process of syncing GitHub user information with Freshdesk contacts, allowing for seamless management of customer data across platforms.

## Prerequisites

Before running the program, ensure you have the following set up:
- **GitHub Token**: Obtain a personal access token from GitHub with the necessary permissions to access user data.
- **Freshdesk Token**: Generate a personal access token from Freshdesk with permissions to manage contacts.

## Setup

1. Clone the repository to your local machine:

2. Navigate to the project directory

3. Set up environment variables for your tokens on your system

```bash
export GITHUB_TOKEN=your_github_token_here
export FRESHDESK_TOKEN=your_freshdesk_token_here
```
4. Download the necessary requirement libraries from the **requirements.txt** file

5. Run the script - it will prompt you to enter a Command, GitHub username and a Freshdesk subdomain

6. Enter the GitHub username from which you want to pull data | | | Enter the Freshdesk subdomain where you wish to create, update or delete the contact.

## Features

- **DataBase Logging:** Captures the username and time of contact additions in Freshdesk and stores them in a database for future reference.
- **GitHub Integration:** Fetches detailed user information from GitHub
- **Freshdesk Integration:** Uses the Freshdesk API to create,update or delete contacts based on the retrieved GitHub information.
- **Error Handling:** Includes robust error handling and retry mechanisms to ensure reliability.
- **Engine:** Implements an engine to orchestrate the flow of commands and interactions
- **Command Factory:** Utilizes a command factory pattern to abstract the creation of API requests and responses.

## Future Work

This program can be extended to include additional functionalities such as:

- **Verifying a specific contact**
- **Blocking a specific contact**
- **Making a whole ticket system**

### [Click to return to the top](#introduction)