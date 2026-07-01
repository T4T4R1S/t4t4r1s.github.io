document.addEventListener("DOMContentLoaded", function() {
  const blockquotes = document.querySelectorAll("blockquote");

  blockquotes.forEach(blockquote => {
    const firstP = blockquote.querySelector("p");
    if (!firstP) return;

    const html = firstP.innerHTML;
    const lines = html.split(/<br\s*\/?>|\n/i);
    const firstLine = lines[0];
    
    // Pattern to match [!TYPE] optionally followed by + or - and optional title
    const match = firstLine.match(/^\[!([a-zA-Z0-9]+)\]([+-]?)(?:\s+(.*))?/i);
    if (match) {
      const type = match[1].toLowerCase();
      const collapseIndicator = match[2];
      const titleHtml = match[3] || type.charAt(0).toUpperCase() + type.slice(1);

      // reconstruct the rest of the paragraph
      lines.shift(); // remove the first line
      const remainingHtml = lines.join('<br>');
      if (remainingHtml.trim() === '') {
          firstP.style.display = 'none'; // hide empty paragraph
      } else {
          firstP.innerHTML = remainingHtml;
      }

      blockquote.classList.add("callout", `callout-${type}`);
      
      const titleDiv = document.createElement("div");
      titleDiv.className = "callout-title";

      // Add SVG icons depending on type
      let iconSvg = '';
      if (['note', 'info'].includes(type)) {
        iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>';
      } else if (['tip', 'success'].includes(type)) {
        iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>';
      } else if (['warning', 'caution'].includes(type)) {
        iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>';
      } else if (['danger', 'error', 'bug'].includes(type)) {
        iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>';
      } else if (['question'].includes(type)) {
        iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>';
      } else {
        iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>';
      }

      titleDiv.innerHTML = `<span class="callout-icon">${iconSvg}</span><span class="callout-title-text">${titleHtml}</span>`;
      
      const contentDiv = document.createElement("div");
      contentDiv.className = "callout-content";
      
      // Move all children of blockquote into contentDiv
      while (blockquote.firstChild) {
        contentDiv.appendChild(blockquote.firstChild);
      }
      
      blockquote.appendChild(titleDiv);
      blockquote.appendChild(contentDiv);

      // Handle collapsible
      if (collapseIndicator === '-' || collapseIndicator === '+') {
        blockquote.classList.add("callout-collapsible");
        const chevron = document.createElement("span");
        chevron.className = "callout-fold";
        chevron.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>';
        titleDiv.appendChild(chevron);
        
        if (collapseIndicator === '-') {
          blockquote.classList.add("callout-collapsed");
        }
        
        titleDiv.addEventListener("click", () => {
          blockquote.classList.toggle("callout-collapsed");
        });
      }
    }
  });
});
