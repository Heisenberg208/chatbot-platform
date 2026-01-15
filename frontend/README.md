# Chatbot Platform - React Frontend (Updated & Secured)

A modern React frontend with **security vulnerabilities fixed** and ESLint warnings resolved.

## ✅ What's Fixed

- **Updated dependencies** to latest secure versions
- **Fixed React Hook warnings** using `useCallback`
- **Added dependency overrides** for transitive vulnerabilities
- **Clean npm audit** - no critical vulnerabilities
- **Updated axios** to latest version (1.7.9)

## Quick Start

### Installation

```bash
cd frontend
npm install
```

### Start Development Server

```bash
npm start
```

Opens at `http://localhost:3000`

## Security Updates

This version includes:

1. **Updated React Scripts** with security patches
2. **Dependency Overrides** for vulnerable transitive dependencies:
   - `nth-check` → 2.1.1+
   - `postcss` → 8.4.31+
   - `webpack-dev-server` → 5.2.1+
3. **Latest Axios** (1.7.9) with security fixes

## Clean Installation

If you had the old version installed:

```bash
# Remove old dependencies
rm -rf node_modules package-lock.json

# Fresh install
npm install

# Verify no critical vulnerabilities
npm audit
```

## Verification

After installation, you should see:

```bash
npm audit
# found 0 vulnerabilities (or only low-severity)
```

## ESLint Warnings Fixed

✅ **Fixed:** React Hook `useEffect` dependency warnings by using `useCallback`
✅ **No more warnings** during compilation

## Development

All features from the original version:
- ✅ Authentication (login/register)
- ✅ Project management
- ✅ System prompts
- ✅ Chat interface with **proper isolation per project**
- ✅ Clean, modern UI

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── AuthPage.js
│   │   ├── Sidebar.js
│   │   ├── ChatInterface.js
│   │   ├── PromptsManager.js         # Fixed hooks
│   │   └── CreateProjectModal.js
│   ├── services/
│   │   └── api.js
│   ├── App.js                         # Fixed hooks
│   ├── App.css
│   └── index.js
├── package.json                       # Updated dependencies
├── .env.example
└── .gitignore
```

## Environment Configuration

Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Production Build

```bash
npm run build
```

Creates optimized build in `build/` folder.

## Troubleshooting

### Still seeing vulnerabilities?

1. Delete `node_modules` and `package-lock.json`:
   ```bash
   rm -rf node_modules package-lock.json
   ```

2. Clear npm cache:
   ```bash
   npm cache clean --force
   ```

3. Reinstall:
   ```bash
   npm install
   ```

### Audit shows warnings but not errors?

The package.json includes `overrides` to force secure versions of transitive dependencies. Some warnings may still appear for dev dependencies that don't affect production.

### CORS Issues?

Ensure your FastAPI backend has proper CORS configuration:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## What Changed from v1?

1. **package.json**: Updated all dependencies, added overrides
2. **App.js**: Added `useCallback` to fix ESLint warnings
3. **PromptsManager.js**: Added `useCallback` to fix ESLint warnings
4. **Functionality**: Everything else remains the same

## Scripts

- `npm start` - Start development server
- `npm build` - Create production build  
- `npm test` - Run tests
- `npm run eject` - Eject from CRA (not recommended)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

MIT
