import requests
def add(a,b):
    return a+b
def avg(nums):
    if not nums:
        return 0
    return sum(nums)/len(nums)
if __name__ == '__main__':
    print("自测：", add(2, 3), avg([1, 2, 3]))
def safe_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
def fetch_repo_count(username):
    try:
        r = requests.get(
            f"https://api.github.com/users/{username}",
            timeout=10,
        )
        r.raise_for_status()
        return r.json().get("public_repos")
    except requests.Timeout:
        return "请求超时"
    except requests.HTTPError as e:
        return f"HTTP 错误：{e.response.status_code}"
    except Exception as e:
        return f"未知错误：{e}"