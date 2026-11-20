# Quick setup model defaults

Checked 2026-11-21 (Asia/Taipei). Defaults target current general text model families suitable for letter polishing; they do not overwrite saved providers on startup. The OpenAI-compatible preset has no universal model ID and remains manually configurable.

| Provider | API model ID | Official reference |
| --- | --- | --- |
| OpenAI | `gpt-6.2-sol` | https://developers.openai.com/api/docs/models/gpt-6.2-sol.md |
| Anthropic | `claude-sonnet-5-5` | https://platform.claude.com/docs/en/models/overview |
| Google | `gemini-3.8-flash` | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash |
| Groq | `openai/gpt-oss-120b` | https://console.groq.com/docs/models |
| DeepSeek | `deepseek-flash` | https://api-docs.deepseek.com/quick_start/pricing/ |

Google's API Studio documentation redirected to an empty response during the check. The official Google Cloud model page confirms the exact ID and GA status; live API entitlement was not tested. Other defaults were checked against their respective official model listings. No paid API credentials were used.

Reasoning GPT requests omit arbitrary temperature. Claude 5 requests omit temperature and collect text blocks from the response. Older/custom model formats retain their existing sampling setting. Requests were checked with mocked responses, not paid live completions.
