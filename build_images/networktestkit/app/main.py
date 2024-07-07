from fastapi import FastAPI, Response, Body, Depends, HTTPException
from pydantic import BaseModel, field_validator
import asyncio
import telnetlib3
import aiohttp
import dns.resolver

app = FastAPI()


class TelnetInfo(BaseModel):
    host: str
    port: int

    @field_validator('host')
    def validate_host(cls, value):
        if not value:
            raise ValueError("host cannot be empty")
        return value

    @field_validator('port')
    def validate_port(cls, value):
        if value is None or value <= 0 or value > 65535:
            raise ValueError("port must be a positive integer between 1 and 65535")
        return value


class RequestUrl(BaseModel):
    url: str

    @field_validator('url')
    def validate_url(cls, value):
        if not value:
            raise ValueError("url cannot be empty")
        return value


class DNSLookupRequest(BaseModel):
    hostname: str

    @field_validator('hostname')
    def validate_hostname(cls, value):
        if not value:
            raise ValueError("hostname cannot be empty")
        return value


async def perform_dns_lookup(request: DNSLookupRequest) -> list[str]:
    resolver = dns.resolver.Resolver()
    try:
        answers = resolver.resolve(request.hostname, "A")
        return [str(answer.address) for answer in answers]
    except dns.resolver.NXDOMAIN:
        raise HTTPException(status_code=404, detail=f"Hostname {request.hostname} does not exist")
    except dns.exception.DNSException as e:
        raise HTTPException(status_code=500, detail=f"DNS error: {e}")


@app.post("/dnslookup")
async def lookup_hostname(hostname: str = Depends(perform_dns_lookup)):
    if not hostname:
        return {"error": "Hostname is required"}

    ip_addresses = hostname
    return {"message": f"Resolved addresseses: {', '.join(ip_addresses)}"}


@app.post("/urlrequest")
async def perform_url_request(url_data: RequestUrl):
    async with aiohttp.ClientSession() as session:  # Use asynchronous session
        try:
            async with session.get(url_data.url) as response:
                response.raise_for_status()  # Raise for non-200 status codes
                content = await response.text()
                return {"message": f"Connection Established! Retrieved data from {url_data.url}", "content": content}
        except aiohttp.ClientError as e:
            return Response(content=f"Error: {str(e)}", status_code=500)
        except Exception as e:  # Catch other potential exceptions
            return Response(content=f"Error: {str(e)}", status_code=500)


@app.post("/telnet")
async def perform_telnet_connection(info: TelnetInfo = Body(...)):
    try:
        await asyncio.wait_for(telnetlib3.open_connection(info.host, info.port), 5)
        return {"message": f"Connection Established for host:{info.host}, port:{info.port}!"}
    except (asyncio.exceptions.TimeoutError, OSError) as e:
        return {"message": f"Connection Error for host:{info.host}, port:{info.port}: {e}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
