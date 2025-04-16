import requests
import argparse
import time
import random
from concurrent.futures import ThreadPoolExecutor

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

def print_status(code, url, verbose, clean, color=False):
    message = f"{code} - {url}"
    if color and COLORAMA_AVAILABLE:
        if code == 200:
            print(Fore.GREEN + f"✅ Found: {message}")
        elif code in [301, 302]:
            print(Fore.YELLOW + f"🔁 Redirect: {message}")
        elif code == 403:
            print(Fore.MAGENTA + f"🚫 Forbidden: {message}")
        elif code == 401:
            print(Fore.CYAN + f"🔐 Unauthorized: {message}")
        elif code == 404 and verbose:
            print(Fore.RED + f"❌ Not Found: {message}")
        elif code == 500 and verbose:
            print(Fore.RED + Style.BRIGHT + f"💥 Server Error: {message}")
        elif verbose:
            print(Fore.WHITE + f"ℹ️ {message}")
    else:
        if code in [200, 301, 302, 403]:
            print(f"✅ Found: {message}")
        elif verbose and not clean:
            if code == 404:
                print(f"❌ 404 Not Found: {url}")
            elif code == 401:
                print(f"🔐 401 Unauthorized: {url}")
            elif code == 500:
                print(f"🔥 500 Server Error: {url}")
            else:
                print(f"ℹ️ {message}")

def scan_directory(base_url, directory, headers, verbose, clean, results, use_color, retry_count, rate_limit):
    target_url = f"{base_url.rstrip('/')}/{directory}"
    retries = 0
    while retries <= retry_count:
        try:
            response = requests.get(target_url, headers=headers, timeout=5)
            code = response.status_code
            if code in [200, 301, 302, 403]:
                results.append(f"{code} - {target_url}")
            print_status(code, target_url, verbose, clean, use_color)
            if rate_limit > 0:
                time.sleep(random.uniform(0, rate_limit))
            break
        except requests.exceptions.RequestException:
            retries += 1
            if retries > retry_count:
                print(f"⚠️ Failed: {target_url}")
            else:
                time.sleep(1)

def brute_force_directories(url, wordlist, output_file=None, verbose=False, clean=False,
                            threads=10, use_color=False, retry_count=3, rate_limit=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (DirBrute/1.0)'
    }

    try:
        with open(wordlist, 'r') as f:
            directories = f.read().splitlines()
    except FileNotFoundError:
        print(f"❗ Wordlist file not found: {wordlist}")
        return

    print(f"\n🚀 Scanning {url} with {threads} threads...\n")
    results = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for directory in directories:
            executor.submit(scan_directory, url, directory, headers, verbose, clean, results,
                            use_color, retry_count, rate_limit)

    time.sleep(1)
    if output_file:
        with open(output_file, 'w') as f:
            for line in results:
                f.write(line + "\n")
        print(f"\n📁 Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🕵️ Threaded Directory Brute Forcer")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com)")
    parser.add_argument("-w", "--wordlist", default="common.txt", help="Wordlist file (default: common.txt)")
    parser.add_argument("-o", "--output", help="Save found directories to file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode (show all status codes)")
    parser.add_argument("-c", "--clean", action="store_true", help="Clean mode: only show found directories")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("--color", action="store_true", help="Enable colored output")
    parser.add_argument("-r", "--retry", type=int, default=3, help="Number of retries on failure (default: 3)")
    parser.add_argument("--rate", type=float, default=1, help="Rate limit (delay between requests in seconds, default: 1)")
    parser.add_argument("-f", "--fast", nargs='?', const=100, type=int, help="Fast mode: no retries/delay, use N threads (default 100)")

    args = parser.parse_args()

    if args.fast is not None:
        args.retry = 0
        args.rate = 0
        args.threads = args.fast
        print(f"⚡ Fast mode enabled: No delay, No retry, {args.threads} threads")

    brute_force_directories(
        url=args.url,
        wordlist=args.wordlist,
        output_file=args.output,
        verbose=args.verbose,
        clean=args.clean,
        threads=args.threads,
        use_color=args.color,
        retry_count=args.retry,
        rate_limit=args.rate
    )
