# ShadowBurst

ShadowBurst is a Python-based Directory Brute Forcer that uses multithreading to quickly discover hidden directories on a target URL. It features options like retries, rate limiting, colorized output, and custom thread counts to give you a fast and customizable directory scanning experience.

# Installation

1 . Clone the repository:

Clone the ShadowBurst project to your local machine using the following command:

```bash
git clone https://github.com/yourusername/ShadowBurst.git
```
2 . Navigate into the project directory:

```bash
cd ShadowBurst
```

3 . Install dependencies:

Make sure you have pip installed, then install the required dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```
# Usage
To run the ShadowBurst tool, use the following command syntax:

```bash
python3 ShadowBurst.py -u [TARGET_URL] -w [WORDLIST_FILE] [OPTIONS]
```
# Required Arguments:
-u  : Target URL to scan (e.g., https://example.com)

-w  : Path to your wordlist (e.g., common.txt)

# Optional Arguments:
-o  OUTPUT_FILE   : Save the found directories to a file.

-v  --verbose     : Show all status codes (not just found ones).

-c  --clean       : Only show found directories (no 404s, etc.).

-t  --threads [NUMBER]   : Number of threads to use (default is 10).

--color           : Enable colored output for better visualization (requires colorama).

-r  --retry [NUMBER]   : Set the number of retries for failed requests (default is 3).

--rate [SECONDS]  : Set the rate limit (time in seconds between requests, default is 1).

-f  --fast [THREADS]   : Enable fast mode with no retries or delays, using a high number of threads (default is 100).

# Example Commands:
1 . Standard scan with 10 threads:

```bash
python3 ShadowBurst.py -u https://example.com -w common.txt
```
2 . Scan with color output:

```bash
python3 ShadowBurst.py -u https://example.com -w common.txt --color
```

3 . Scan with retries and rate limiting:

```bash
python3 ShadowBurst.py -u https://example.com -w common.txt -r 5 --rate 0.5
```
4 . Fast scan with 200 threads:

```bash
python3 ShadowBurst.py -u https://example.com -w common.txt -f 200
```

