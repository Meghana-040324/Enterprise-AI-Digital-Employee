"""FastAPI entry point."""
import time

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from models import (
    AITaskRequest,
    AITaskResponse,
    IncidentRequest
)

from services.openai_service import (
    openai_service
)

from services.memory_service import (
    memory_service
)

from services.incident_service import (
    incident_service
)

from services.document_service import (
    document_service
)

from services.analytics_service import (
    analytics_service
)


app = FastAPI(

    title=
        "Enterprise AI Digital Employee",

    description=
        "AI-powered enterprise "
        "automation platform",

    version=
        "4.0.0"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"]
)


@app.get("/")
async def root():

    return {

        "status":
            "online",

        "application":
            "Enterprise AI "
            "Digital Employee",

        "version":
            "4.0.0"
    }


@app.get("/health")
async def health():

    return {
        "status":
            "healthy"
    }


@app.post(
    "/process-ai",
    response_model=AITaskResponse
)
async def process_ai_task(
    request: AITaskRequest
):

    start = time.perf_counter()

    prompt = (
        request.prompt.strip()
    )

    if not prompt:

        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty."
        )

    action = "chat"

    incident_number = None

    try:

        action = (
            openai_service
            .detect_action(
                prompt
            )
        )

        if action == "incident":

            incident = (
                incident_service
                .create_incident(

                    short_description=
                        prompt,

                    description=
                        "Created automatically "
                        "by Enterprise AI "
                        "Digital Employee."
                )
            )

            if incident.get(
                "success"
            ):

                incident_number = (
                    incident.get(
                        "number"
                    )
                )

                analytics_service.record_incident()

                ai_response = (
                    "Your IT issue was "
                    "identified and an "
                    "incident was created "
                    "successfully."
                )

                if incident_number:

                    ai_response += (
                        f"\n\nIncident: "
                        f"{incident_number}"
                    )

            else:

                fallback = (
                    openai_service
                    .generate_response(

                        prompt=
                            prompt,

                        session_id=
                            request.session_id,

                        persona=
                            request.persona
                    )
                )

                ai_response = (
                    f"{fallback}\n\n"
                    "I identified this as "
                    "an IT incident, but "
                    "automatic ServiceNow "
                    "incident creation is "
                    "currently unavailable."
                )

        else:

            ai_response = (
                openai_service
                .generate_response(

                    prompt=
                        prompt,

                    session_id=
                        request.session_id,

                    persona=
                        request.persona
                )
            )

        elapsed = (
            time.perf_counter()
            - start
        ) * 1000

        analytics_service.record_request(

            success=True,

            execution_time_ms=
                elapsed,

            action=
                action
        )

        return AITaskResponse(

            status=
                "success",

            response=
                ai_response,

            executionTimeMs=
                round(
                    elapsed,
                    2
                ),

            action=
                action,

            incident_number=
                incident_number
        )

    except Exception as exc:

        elapsed = (
            time.perf_counter()
            - start
        ) * 1000

        analytics_service.record_request(

            success=False,

            execution_time_ms=
                elapsed,

            action=
                action
        )

        raise HTTPException(

            status_code=500,

            detail=str(exc)
        )


@app.post("/incidents")
async def create_incident(
    request: IncidentRequest
):

    result = (
        incident_service
        .create_incident(

            short_description=
                request.short_description,

            description=
                request.description
                or "",

            urgency=
                request.urgency,

            impact=
                request.impact
        )
    )

    if result.get(
        "success"
    ):

        analytics_service.record_incident()

    return result


@app.post("/documents/upload")
async def upload_document(

    file: UploadFile =
        File(...)
):

    try:

        document = (
            await document_service
            .save_and_extract(
                file
            )
        )

        analytics_service.record_document()

        return {

            "success":
                True,

            "document_id":
                document["id"],

            "filename":
                document["filename"],

            "characters":
                len(
                    document["text"]
                ),

            "message":
                "Document uploaded "
                "and processed."
        }

    except ValueError as exc:

        raise HTTPException(

            status_code=400,

            detail=str(exc)
        )


@app.delete(
    "/memory/{session_id}"
)
async def clear_memory(
    session_id: str
):

    memory_service.clear(
        session_id
    )

    return {

        "success":
            True,

        "message":
            "Conversation cleared."
    }


@app.get("/analytics")
async def analytics():

    return (
        analytics_service
        .get_stats()
    )


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host=
            "0.0.0.0",

        port=
            8000,

        reload=
            True
    )