
const BASE_URL = "https://aeonanalyzer.onrender.com";

/**
 * Extracts the essay URL from the query string.
 * @returns {string|null}
 */
function getEssayUrlFromQuery() {
  const params = new URLSearchParams(window.location.search);
  return params.get("url");
}

/**
 * Fetches the essay content from the backend and renders it in the DOM.
 */
async function fetchEssay() {
  const url = getEssayUrlFromQuery();

  const titleElem = document.getElementById("essay-title");
  const subheadingElem = document.getElementById("essay-subheading");
  const authorElem = document.getElementById("essay-author");
  const contentElem = document.getElementById("essay-content");

  if (!url) {
    contentElem.innerHTML = `<p style="color: red;">❌ No URL provided.</p>`;
    return;
  }

  try {
    
    const response = await fetch(`${BASE_URL}/essay-content?url=${encodeURIComponent(url)}`);
    if (!response.ok) throw new Error("Failed to fetch essay content.");
    
    const data = await response.json();

    titleElem.textContent = data.title || "Untitled";
    subheadingElem.textContent = data.subheading || "";
    authorElem.textContent = data.author || "Unknown author";
    contentElem.innerHTML = data.content || "<p>No content found.</p>";
  } catch (err) {
    contentElem.innerHTML = `<p style="color: red;">❌ Error: ${err.message}</p>`;
  }
}

/**
 * Calls the backend to analyze the essay and renders the AI-generated insights.
 * Only hides the button if successful.
 */
async function fetchAIAnalysis() {
  const url = getEssayUrlFromQuery();
  const aiPanel = document.querySelector(".ai-output");
  const analyzeBtn = document.getElementById("analyzeBtn");

  if (!url || !aiPanel || !analyzeBtn) return;

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";

  try {
    const response = await fetch(`${BASE_URL}/analyze-essay?url=${encodeURIComponent(url)}`);
    const analysis = await response.json();

    if (!response.ok || analysis.error || !analysis) {
      // Failure: show error, don't hide button
      const message = analysis.error
        ? `❌ Error: ${analysis.error}`
        : `❌ Server Error (${response.status}): ${response.statusText}`;
      aiPanel.innerHTML = `<p style="color:red;">${message}</p>`;
      analyzeBtn.disabled = false;
      analyzeBtn.textContent = "Run AI Analysis";
      return;
    }

    // ✅ Success: Render and hide button
    aiPanel.innerHTML = renderAIInsights(analysis);
    analyzeBtn.classList.add("hidden");

  } catch (err) {
    aiPanel.innerHTML = `<p style="color: red;">❌ Network error: ${err.message}</p>`;
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Run AI Analysis";
  }
}

/**
 * Renders AI insights into HTML.
 * @param {Object} analysis
 * @returns {string}
 */
function renderAIInsights(analysis) {
  function renderList(list) {
    if (!Array.isArray(list)) return "Not available";
    return `<ul>${list.map(item => `<li>${item}</li>`).join("")}</ul>`;
  }

  return `
    <div class="ai-section"><h3>Summary</h3><div>${analysis.summary ?? "Not available"}</div></div>
    <div class="ai-section"><h3>Genre</h3><div>${analysis.genre ?? "Not available"}</div></div>
    <div class="ai-section"><h3>Classification</h3><div>${analysis.classification ?? "Not available"}</div></div>
    <div class="ai-section"><h3>Main Point</h3><div>${analysis.main_point ?? "Not available"}</div></div>
    <div class="ai-section"><h3>Supporting Arguments</h3><div>${renderList(analysis.supporting_arguments)}</div></div>
    <div class="ai-section"><h3>Contrasting Views</h3><div>${renderList(analysis.contrasting_views)}</div></div>
    <div class="ai-section"><h3>Paragraph Summaries</h3><div>${renderList(analysis.paragraph_summaries)}</div></div>
  `;
}

/**
 * Navigates to essay.html with the given URL as query string.
 */
function goToEssayPage() {
  const input = document.getElementById("urlInput");
  const url = input.value.trim();

  if (!url) {
    alert("⚠️ Please paste a valid Aeon essay URL.");
    return;
  }

  window.location.href = `/essay.html?url=${encodeURIComponent(url)}`;
}

/**
 * Initializes the page logic depending on the current page.
 */
window.addEventListener("DOMContentLoaded", () => {
  const isEssayPage = document.getElementById("essay-content") !== null;

  if (isEssayPage) {
    fetchEssay();
    const btn = document.getElementById("analyzeBtn");
    if (btn) {
      btn.addEventListener("click", fetchAIAnalysis);
    }
  }
});


