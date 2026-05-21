const keywordFallback = (complaint) => {
  const text = `${complaint.title} ${complaint.description} ${complaint.category}`.toLowerCase();
  let urgency = "Medium";
  let department = "General Administration";

  if (text.includes("electric") || text.includes("fire") || text.includes("danger")) {
    urgency = "High";
    department = "Electricity Department";
  } else if (text.includes("water") || text.includes("leak") || text.includes("pipeline")) {
    urgency = "High";
    department = "Water Supply Department";
  } else if (text.includes("garbage") || text.includes("waste") || text.includes("clean")) {
    urgency = "Medium";
    department = "Sanitation Department";
  } else if (text.includes("road") || text.includes("traffic") || text.includes("street")) {
    department = "Public Works Department";
  }

  return {
    urgency,
    department,
    summary: `${complaint.title}: ${complaint.description.slice(0, 120)}${
      complaint.description.length > 120 ? "..." : ""
    }`,
    response: `Your complaint has been registered and forwarded to the ${department}. Current priority is ${urgency}.`
  };
};

const parseAiJson = (content, complaint) => {
  try {
    const jsonStart = content.indexOf("{");
    const jsonEnd = content.lastIndexOf("}");
    const jsonText = content.slice(jsonStart, jsonEnd + 1);
    const parsed = JSON.parse(jsonText);

    return {
      urgency: parsed.urgency || "Medium",
      department: parsed.department || "General Administration",
      summary: parsed.summary || complaint.description,
      response: parsed.response || "Your complaint has been received."
    };
  } catch (error) {
    return keywordFallback(complaint);
  }
};

const analyzeComplaintText = async (complaint) => {
  if (!process.env.OPENROUTER_API_KEY) {
    return keywordFallback(complaint);
  }

  try {
    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "Smart Complaint Management System"
      },
      body: JSON.stringify({
        model: process.env.OPENROUTER_MODEL || "openai/gpt-4o-mini",
        messages: [
          {
            role: "system",
            content:
              "Analyze civic complaints. Return only JSON with urgency, department, summary, and response."
          },
          {
            role: "user",
            content: JSON.stringify({
              title: complaint.title,
              description: complaint.description,
              category: complaint.category,
              location: complaint.location
            })
          }
        ],
        temperature: 0.2
      })
    });

    if (!response.ok) {
      return keywordFallback(complaint);
    }

    const data = await response.json();
    const content = data.choices?.[0]?.message?.content || "";
    return parseAiJson(content, complaint);
  } catch (error) {
    return keywordFallback(complaint);
  }
};

const analyzeComplaintFromBody = async (req, res, next) => {
  try {
    const analysis = await analyzeComplaintText(req.body);
    res.json({ message: "AI analysis completed.", analysis });
  } catch (error) {
    next(error);
  }
};

module.exports = { analyzeComplaintFromBody, analyzeComplaintText };
