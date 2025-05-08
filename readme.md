# Copilot Proxy

My personal fork of Copilot Proxy so that I can safely interface Aider with GitHub Copilot's LM API's.

## Aider Configuration

The following is an example `.aider.model.settings.yml` which you
can put either in your home directory (likely the best option) or
another supported location.

```
# The below are custom configuration files that allow for Aider
# to interact with alterantive server endpoints. This particular
# configuration is for all available supported models as of
# May 8th, 2025. Support was tested both locally and with Cline.
# NOTE: this means that not all models returned by the Copilot LM
# API are actually functional.

- name: claude-3-5-sonnet-latest
  extra_params:
    model: openai/claude-3.5-sonnet
    api_key: n/a
    api_base: http://localhost:3000/v1

- name: gpt-4o
  extra_params:
    api_key: n/a
    api_base: http://localhost:3000/v1

- name: gpt-4o-mini
  extra_params:
    api_key: n/a
    api_base: http://localhost:3000/v1

- name: o3-mini
  extra_params:
    api_key: n/a
    api_base: http://localhost:3000/v1

- name: gpt-4.1
  extra_params:
    model: gpt-4.1
    api_key: n/a
    api_base: http://localhost:3000/v1

- name: o1
  extra_params:
    model: openai/o1-ga
    api_key: n/a
    api_base: http://localhost:3000/v1

# This applies to all models, but really only works for OpenAI models largely.
# It is kept here for legacy reasons, but all models I could find that
# were supported by CoPilot Proxy (and tested in  Cline) are explicitly
# defined above.
- name: aider/extra_params
  extra_params:
    api_key: n/a
    api_base: http://localhost:3000/v1
```

## Code Review for Malware

I personally reviewed the code, and found no evidence of malware. I also had Gemini 2.5 Pro review it, and here is Gemini's summary.

#### inspect this repository for evidence of malware

Okay, I have reviewed the contents of the files you've provided: `.gitignore`, `LICENSE`, `environment.yaml`, `package.json`, `readme.md`, `src/client/client.py`, `src/client/requirements.txt`, `src/client/run_client.sh`, `src/extension.ts`, `src/server.ts`, `src/types.ts`, and `tsconfig.json`.

Here's my inspection for evidence of malware:

1.  **`package.json`**:

    - **Dependencies**:
      - `dotenv`: Used for loading environment variables. Standard and safe.
      - `express`: A very common web framework for Node.js. Standard and safe.
      - `morgan`: An HTTP request logger middleware for Node.js. Standard and safe.
    - **DevDependencies**:
      - `@types/*`: Type definitions for TypeScript. Standard and safe.
      - `ts-node`: Allows direct execution of TypeScript files. Standard for development.
      - `typescript`: The TypeScript compiler. Standard.
      - `vsce`: The official tool for packaging VS Code extensions. Standard.
      - `vscode`: Appears to be an older reference for VS Code API types; `@types/vscode` is more common now but this isn't inherently malicious.
    - **Scripts**:
      - `build`, `start`, `vsix`, `test_client`: These scripts use standard commands (`tsc`, `ts-node`, `vsce`, `cd`, `./run_client.sh`) for building, running, packaging the extension, and testing the client. The `test_client` script correctly executes the local shell script.
    - **Repository URL**: `https://github.com/yourusername/copilot-proxy.git` is a placeholder. This is not malicious but indicates it might be a template or not yet fully configured for public release under its final name.
    - **Overall**: The `package.json` file uses standard, well-known packages and scripts for typical development tasks of a VS Code extension. No suspicious dependencies or scripts are evident.

2.  **`src/client/requirements.txt`**:

    - `litellm`: This is a legitimate and popular Python library for simplifying calls to various LLM APIs.
    - **Overall**: Clean.

3.  **`src/client/run_client.sh`**:

    - Sets `OPENAI_API_KEY="n/a"` and `OPENAI_API_BASE="http://localhost:3000/v1"`. This correctly configures the LiteLLM client to use the local proxy server running on port 3000, which is the purpose of this project.
    - Executes `python client.py`.
    - **Overall**: This script is benign and serves its intended purpose of testing the client against the local proxy.

4.  **`src/client/client.py`**:

    - Imports `os` and `litellm.completion`.
    - Defines functions `run_litellm_non_stream` and `run_litellm_stream` that make calls to `litellm.completion` with a hardcoded prompt ("Create a fibonacci function in Python") and model ("gpt-4o").
    - It relies on environment variables (set by `run_client.sh`) for `api_base` and `api_key`.
    - Prints responses to the console.
    - **Overall**: This is a straightforward test client. It does not perform any suspicious operations, file access, or network calls beyond what's configured for LiteLLM (which is to the local proxy).

5.  **`src/extension.ts`**:

    - Manages the lifecycle of an Express server (`startServer`, `serverInstance.close`).
    - Uses `vscode.window.createOutputChannel` for logging, which is standard for VS Code extensions. Logs include request details, which is useful for debugging a proxy.
    - `configurePort` function allows users to change the port via VS Code settings, which is a legitimate feature.
    - `processChatRequest`:
      - Extracts message content using `extractMessageContent`, which handles simple string and structured array content.
      - Maps incoming messages to `vscode.LanguageModelChatMessage` format.
      - Uses `vscode.lm.selectChatModels` and `selectedModel.sendRequest` to interact with the VS Code Language Model API (Copilot). This is the core, legitimate functionality.
      - For streaming requests, it iterates over `chatResponse.text` and yields chunks formatted as `ChatCompletionChunk`.
      - For non-streaming requests, it accumulates the response and formats it as `ChatCompletionResponse`.
      - Error handling logs errors to the output channel.
    - **Overall**: The extension code appears to be a clean implementation of a proxy. It uses official VS Code APIs as intended. There's no evidence of data exfiltration to unauthorized locations, obfuscated code, or execution of arbitrary commands.

6.  **`src/server.ts`**:
    - Uses Express to create an HTTP server.
    - Uses `dotenv` for environment variables and `morgan` for logging HTTP requests to the console. Both are standard.
    - The main endpoint `/v1/chat/completions`:
      - Parses the request body.
      - The line `req.body.model = model.split('/').pop()!;` is a legitimate transformation to extract the base model name (e.g., "claude-3.5-sonnet" from "openrouter/anthropic/claude-3.5-sonnet") for compatibility with the Copilot API.
      - If `stream` is true, it sets appropriate headers for Server-Sent Events (SSE) and streams chunks from `processChatRequest`. It correctly writes data

> Tokens: 6.3k sent, 1.2k received.

# Original

## Overview

Copilot Proxy is a Visual Studio Code extension that exposes the VS Code Language Model API via an Express server. This experimental extension is intended solely for research and prototyping purposes and should not be used in production environments.

[![Watch the video](https://img.youtube.com/vi/i1I2CAPOXHM/maxresdefault.jpg)](https://youtu.be/i1I2CAPOXHM)
[YouTube Explanation](https://youtu.be/i1I2CAPOXHM)

**Disclaimer:**  
This extension is provided as an experiment only. In the past, some users, i.e., cline users, faced bans due to excessive usage. Since Microsoft introduced rate limits to the VS Code LM, no further bans have been reported. Nevertheless, I do not recommend using this extension for anything beyond research and prototyping.

At the moment, the supported LLMs by GitHub Copilot are: "gpt-4o", "gpt-4o-mini", "o1", "o1-mini", "claude-3.5-sonnet", and "o3-mini".

## Features

- **Server Management:** Easily start and stop the Express server from within VS Code.
- **Customizable Port:** Configure the port the server uses through VS Code settings or via an interactive command.
- **Language Model Integration:** Relay chat-based requests and responses with support for both streaming and non-streaming modes.

## Installation

1. **Download the VSIX Package:**

- Visit the [GitHub Releases](https://github.com/lutzleonhardt/copilot-proxy/releases) page.
- Download the latest `.vsix` file.

2. **Install the Extension:**

- Open Visual Studio Code.
- Go to the Extensions view (`Ctrl+Shift+X` on Windows/Linux or `Cmd+Shift+X` on macOS).
- Click on the three-dot menu (`...`) and choose **"Install from VSIX..."**.
- Select the downloaded `.vsix` file.

3. **Reload VS Code:**

- Accept the prompt to reload the window and activate the extension.

## Configuration

The extension provides a configuration setting to specify the port for the Express server:

- **Setting:** `copilotProxy.port`  
  **Default:** `3000`

You can change this setting in two ways:

- **Via Settings UI:** Open the VS Code Settings (`Ctrl+,` or `Cmd+,`) and search for "Copilot Proxy".
- **Via Command Palette:** Run the command **"Copilot Proxy: Configure Port"** to interactively set the port.

## Using the Extension

### Starting the Server

- Open the Command Palette and run **"Copilot Proxy - Start Server"**.
- The server will start on the configured port (default is `3000`), and a notification will confirm the port.

### Stopping the Server

- Open the Command Palette and run **"Copilot Proxy - Stop Server"** to shut down the server.

### Permission Prompt

On the initial request (e.g., when using Aider or other AI assistants), VS Code will prompt you to grant permission for the extension to interact with the VS Code Language Model API. Please grant permission to ensure proper operation.

### Usage in aider

You need to configure aider to use the proxy server for the chosen models which are supported by GitHub Copilot.
These are at the moment: "gpt-4o", "gpt-4o-mini", "o1", "o1-mini", "claude-3.5-sonnet", and "o3-mini" (also depending on your subscription).
To make this work, you need to create a file `.aider.model.settings.yml` in your home directory or in one of the other supported locations. (see [Configuration file locations](https://aider.chat/docs/config/adv-model-settings.html))

The content of the file should look like this:

```yaml
# "claude-3-5-sonnet-20241022" is the model name used in aider
# "openai/claude-3.5-sonnet"
# => "openai" tells LiteLLM to call an OpenAI-like endpoint
# => "claude-3.5-sonnet" matches the copilot model name
- name: claude-3-5-sonnet-20241022
  extra_params:
    model: openai/claude-3.5-sonnet
    api_key: n/a
    api_base: http://localhost:3000/v1

# "openrouter/anthropic/claude-3.5-sonnet" is the model name used in aider
# "openai/claude-3.5-sonnet"
# => "openai" tells LiteLLM to call an OpenAI-like endpoint
# => "claude-3.5-sonnet" matches the copilot model name
- name: openrouter/anthropic/claude-3.5-sonnet
  extra_params:
    model: openai/claude-3.5-sonnet
    api_key: n/a
    api_base: http://localhost:3000/v1

# "o3-mini" is the model name in aider
# "o3-mini" is already a OpenAI-like API and o3-mini is also matching the name in copilot
- name: o3-mini
  extra_params:
    api_key: n/a
    api_base: http://localhost:3000/v1

# this config is using the copilot LM for ALL models in aider
# BUT this only works for OpenAI-like models and when the name in aider/LiteLLM matches the name in copilot
# so this is mainly working for all supported openai models like GPT-4o, o1, o3-mini
- name: aider/extra_params
  extra_params:
    api_key: n/a
    api_base: http://localhost:3000/v1
```

## Contributing

Contributions, bug reports, and feature requests are welcome! Please submit issues or pull requests in the [GitHub repository](https://github.com/yourusername/copilot-proxy).

## License

This project is licensed under the MIT License.
