# ⚡ QUICK REFERENCE - Fase 3

## 🚀 START SERVER
```bash
cd /Users/admin/Documents/Developer/proyecto-docs
python main.py
```

## 🌐 OPEN IN BROWSER
```
http://localhost:8000
```

## 🧪 RUN TESTS (ALL PASS ✅)
```bash
python test_fase3.py
```

## 📋 WHAT TO TEST

1. **Notes Load**: Go to Biblioteca → Cuaderno → see notes appear ✅
2. **Slash Command**: Type "/" in editor → modal should appear ✅
3. **Type Prompt**: Write your question in modal input
4. **Press Enter**: Send to backend
5. **See Response**: Should appear in modal (blue text)
6. **Click Apply**: Insert response in editor as blue text ✅
7. **Click Retry**: Re-send prompt with same or edited text
8. **Click Close**: Close modal without changing

## 🔍 EXPECTED BEHAVIOR

```
User Types "/"
  ↓
Modal Opens (positioned under cursor)
  ↓
User Types Prompt (e.g., "summarize this")
  ↓
User Presses Enter
  ↓
Modal Shows: "Enviando al backend..."
  ↓
Response Appears in Modal (may take 3-5 seconds)
  ↓
Buttons Appear: [Apply] [Retry] [Close]
  ↓
User Clicks "Apply"
  ↓
Response Inserted in Editor (BLUE TEXT)
  ↓
Modal Closes
  ↓
"/" Disappears and Response Takes Its Place
```

## ✅ VERIFICATION CHECKLIST

- [ ] Server starts without errors
- [ ] Notes load in browser
- [ ] "/" opens modal
- [ ] Modal input is focused (cursor visible)
- [ ] Can type in modal
- [ ] Pressing Enter sends to backend
- [ ] Response appears in modal within 5 seconds
- [ ] Response is NOT red (no error)
- [ ] "Apply" button works
- [ ] Text appears in editor where "/" was
- [ ] Text is BLUE (#60a5fa)
- [ ] Modal closes after Apply
- [ ] Can open "/" again in different position

## 🐛 IF SOMETHING BREAKS

### Notes Won't Load
```bash
# Check browser console (F12)
# Look for errors related to "AIDraft" or "ai-draft"
# Check server logs for Python errors
```

### "/" Won't Open Modal
```bash
# Make sure server is running
# Check console: should see "📍 "/" detectado..."
# Try clicking elsewhere and typing "/" again
```

### Backend Returns Error
```bash
# Check GROQ_API_KEY in .env: should be gsk_xxxxx
# Verify backend is running: curl http://localhost:8000/docs
# Check .env file exists and has valid key
```

### Response Doesn't Appear
```bash
# Check network tab in DevTools (F12)
# POST /api/ai/generate should return 200
# Response should have "response" and "timestamp" fields
```

### Text Not Blue
```bash
# Check DevTools Styles (F12)
# Should have .ai-draft-text styling
# Check that CSS file is linked: look for ai-draft.css in <head>
```

## 📱 BROWSER DEVTOOLS TIPS

### See All Events
```javascript
// In console:
window.addEventListener('ai:command:open', (e) => console.log('📍 OPEN', e.detail));
window.addEventListener('ai:prompt:submit', (e) => console.log('🚀 SUBMIT', e.detail));
window.addEventListener('ai:prompt:apply', (e) => console.log('✅ APPLY', e.detail));
```

### Check Alpine State
```javascript
// In console:
window.Alpine.$data(document.body).aiPrompt
// Should show: { show, x, y, input, response, streaming, slashRange, cursorPos, context }
```

### Manual Backend Test
```bash
# Open new terminal:
curl -X POST http://localhost:8000/api/ai/generate \
  -H "Content-Type: application/json" \
  -d '{
    "noteId": "c2dbfb26-2b0a-45f0-9ec1-be1af514b8cc",
    "content": "Test content",
    "prompt": "summarize this"
  }' | python -m json.tool
```

## 📊 KEY FILES

| File | What It Does | Status |
|------|-------------|--------|
| `static/js/extensions/ai-command.js` | Detects "/" | ✅ |
| `static/js/extensions/ai-draft.js` | Blue text styling | ✅ |
| `static/js/ai-events.js` | Event coordination | ✅ |
| `app/routers/ai.py` | POST /api/ai/generate | ✅ TESTED |
| `app/services/llm_service.py` | Groq API wrapper | ✅ TESTED |

## 🎯 SUCCESS CRITERIA

Fase 3 is complete when:
1. ✅ "/" opens modal (DONE)
2. ✅ Backend receives prompt (DONE)
3. ✅ Groq generates response (DONE)
4. ✅ Response appears in editor (TESTING NOW)
5. ✅ Text is styled as blue draft (TESTING NOW)

## 💾 SAVE LOGS FOR DEBUGGING

If something fails:
```bash
# Capture backend logs:
python main.py 2>&1 | tee server.log

# In browser, open DevTools (F12):
# Right-click → Save as... → console-output.txt
# Include in bug report
```

## 🔑 IMPORTANT NOTES

- **GROQ_API_KEY** must be in `.env` (not committed to git)
- **Model** is llama-3.3-70b-versatile (not deprecated)
- **Event System** is the core - don't break event listeners
- **AIDraft** extension applies blue styling - must be imported
- **slashRange** is critical - it stores where "/" was positioned

## 📞 CONTACTS FOR HELP

- Check: `/docs` - API documentation
- Check: DevTools Console - real-time errors
- Check: `test_fase3.py` - automated validation
- Check: `FASE3_ESTADO_FINAL.md` - technical details

---

**TL;DR**: Start server → Open browser → Type "/" → Get response → Click Apply → Done! ✨

