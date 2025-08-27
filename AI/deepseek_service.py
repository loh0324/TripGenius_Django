# deepseek_service.py
import requests
from typing import Optional, Dict, Any
import json
import logging

# 设置日志
logger = logging.getLogger(__name__)


class DeepSeekService:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        # 验证API密钥
        if not api_key:
            raise ValueError("API密钥不能为空")
            
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        logger.info("DeepSeekService初始化完成")

    def summarize_document(self, document_content: str, custom_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        发送文档到DeepSeek进行总结

        Args:
            document_content: 文档内容
            custom_prompt: 自定义提示词（可选）

        Returns:
            包含总结结果的字典
        """
        try:
            # 确保文档内容是UTF-8编码
            if isinstance(document_content, bytes):
                document_content = document_content.decode('utf-8', errors='ignore')
            else:
                document_content = str(document_content).encode('utf-8', errors='ignore').decode('utf-8')
            
            # 限制文档内容长度以避免API限制
            max_content_length = 20000  # 根据API限制调整
            if len(document_content) > max_content_length:
                document_content = document_content[:max_content_length]
                logger.info(f"文档内容已截断到{max_content_length}字符")

            default_prompt = """请总结以下文档的主要内容，包括关键点和核心信息。
            要求：
            1. 提取主要议题或主题
            2. 列出关键要点
            3. 总结重要数据或结论
            4. 保持逻辑清晰，语言简洁
            
            文档内容如下：
            """
            
            # 确保提示词也是正确的编码
            if custom_prompt:
                if isinstance(custom_prompt, bytes):
                    prompt = custom_prompt.decode('utf-8', errors='ignore')
                else:
                    prompt = str(custom_prompt).encode('utf-8', errors='ignore').decode('utf-8')
            else:
                prompt = default_prompt
            
            full_prompt = f"{prompt}\n{document_content}"
            
            # 确保完整提示词也是UTF-8编码
            full_prompt = full_prompt.encode('utf-8', errors='ignore').decode('utf-8')
            
            logger.info(f"准备发送请求到DeepSeek API，提示词长度: {len(full_prompt)} 字符")

            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "stream": False,
                "temperature": 0.7,
                "max_tokens": 2048
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=120  # 增加超时时间
            )
            
            logger.info(f"收到DeepSeek API响应，状态码: {response.status_code}")
            
            response.raise_for_status()
            result = response.json()
            
            logger.info("成功解析DeepSeek API响应")

            # 确保返回的摘要内容也是正确的编码
            summary = result["choices"][0]["message"]["content"]
            if isinstance(summary, bytes):
                summary = summary.decode('utf-8', errors='ignore')
            else:
                summary = str(summary).encode('utf-8', errors='ignore').decode('utf-8')

            return {
                "success": True,
                "summary": summary,
                "usage": result.get("usage", {})
            }
        except requests.exceptions.Timeout as e:
            logger.error(f"请求DeepSeek API超时: {str(e)}")
            return {
                "success": False,
                "error": "请求DeepSeek API超时，请稍后重试"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"请求DeepSeek API时出错: {str(e)}")
            return {
                "success": False,
                "error": f"请求DeepSeek API时出错: {str(e)}"
            }
        except KeyError as e:
            logger.error(f"解析DeepSeek响应时出错: {str(e)}")
            return {
                "success": False,
                "error": f"解析DeepSeek响应时出错: {str(e)}"
            }
        except UnicodeDecodeError as e:
            logger.error(f"Unicode解码错误: {str(e)}")
            return {
                "success": False,
                "error": "文本编码错误，请确保文件使用标准编码格式"
            }
        except Exception as e:
            logger.error(f"未知错误: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": f"未知错误: {str(e)}"
            }
