# PostgreSQL Analytics Migration - Summary

## Implementation Status: ✅ COMPLETED

### What Was Done

1. **Created PostgreSQL User**
   - Username: `sgnl_analytics`
   - Password: `123456`
   - Database: `sgnl`
   - Permissions: All privileges granted

2. **Updated Environment Configuration**
   - `DATABASE_URL` in `.env`: `postgresql://sgnl_analytics:123456@host.docker.internal:5432/sgnl`
   - `DATABASE_URL` in `docker-compose.yml`: Same as above
   - `DATABASE_URL` in `.env.example`: Same as above

3. **Updated Docker Configuration**
   - Added `extra_hosts` for `host.docker.internal` access
   - Removed SQLite volume mount
   - Updated `docker-compose.yml` default database URL

4. **Updated Dependencies**
   - Added `psycopg2-binary>=2.9.0` to `app/requirements.txt`

5. **Created Analytics System Files**
   - `app/analytics_models.py` - SQLAlchemy models (3 tables)
   - `app/analytics_middleware.py` - Request tracking middleware
   - `app/analytics_routes.py` - API endpoints
   - `app/analytics_utils.py` - Utility functions
   - `app/static/js/analytics.js` - Client-side tracking
   - `init_analytics.py` - Database initialization script

6. **Updated Application Code**
   - Modified `app/main.py` to import and use analytics
   - Added session cookie creation in `/` endpoint

### Database Tables Created

PostgreSQL now has 4 tables:
1. **sgnl_documents** (existing)
2. **visitor_logs** (new)
3. **page_views** (new)
4. **analytics_events** (new)

### Analytics Features

**What Gets Tracked:**
- IP addresses
- User agents (device type: mobile/desktop/tablet/bot)
- Session IDs (cookie-based, 90-day expiry)
- Referrer sources
- Landing pages
- Page views
- Time on page
- Custom events
- Visit timestamps
- Total session time

**API Endpoints:**
- `POST /analytics/track` - Track custom events
- `POST /analytics/heartbeat` - Keep session alive (30s interval)
- `POST /analytics/pageview` - Record page view with time
- `GET /analytics/stats` - Get aggregate statistics
- `GET /analytics/visitors` - Get visitor list
- `POST /analytics/cleanup` - Delete old data (90+ days)

### Current Issues

1. **Session Creation**
   - Session cookies are being created by backend
   - But visitors are not being recorded in database
   - Need to debug why `create_visitor` is not creating records

2. **JavaScript Tracking**
   - `analytics.js` is being served and loaded
   - But client-side tracking might not be working

### Testing Instructions

**Test 1: Check Database Connection**
```bash
# Test if sgnl_analytics user can connect
PGPASSWORD=123456 psql -h localhost -U sgnl_analytics -d sgnl -c "SELECT current_database();"
```

**Test 2: Check Tables**
```bash
sudo -u postgres psql -d sgnl -c "\dt"
```

**Test 3: Check Visitors**
```bash
sudo -u postgres psql -d sgnl -c "SELECT COUNT(*) FROM visitor_logs; SELECT COUNT(*) FROM page_views; SELECT COUNT(*) FROM analytics_events;"
```

**Test 4: Manual Session Creation**
```bash
# Visit homepage
curl -s http://localhost:8000/

# Check if cookie was set
curl -v http://localhost:8000/ 2>&1 | grep -i "set-cookie"

# Check database again
sudo -u postgres psql -d sgnl -c "SELECT session_id, ip_address, created_at FROM visitor_logs ORDER BY created_at DESC LIMIT 5;"
```

**Test 5: API Endpoints**
```bash
# Get stats (returns JSON)
curl -H "Content-Type: application/json" http://localhost:8000/analytics/stats

# Get visitors (returns JSON)
curl -H "Content-Type: application/json" http://localhost:8000/analytics/visitors?limit=10
```

### Next Steps

**Option 1: Debug Session Creation**
Add more detailed logging to `serve_frontend` and `create_visitor` functions:
```python
logger.info(f"[ANALYTICS] Session ID from cookies: {session_id}")
logger.info(f"[ANALYTICS] Creating visitor for IP: {ip}")
logger.info(f"[ANALYTICS] Response cookies: {response.headers.get('set-cookie')}")
```

**Option 2: Simplify Session Flow**
Instead of creating session in backend, let JavaScript handle everything:
1. JavaScript generates session ID
2. JavaScript sets cookie
3. JavaScript sends all tracking data to backend
4. Backend just records data

**Option 3: Manual Testing**
Test each component individually:
1. Test database connection
2. Test analytics API endpoints
3. Test JavaScript loading
4. Test cookie setting
5. Test visitor creation

### Configuration Files

**.env:**
```bash
DATABASE_URL=postgresql://sgnl_analytics:123456@host.docker.internal:5432/sgnl
```

**docker-compose.yml:**
```yaml
services:
  sgnl-api:
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - DATABASE_URL=${DATABASE_URL:-postgresql://sgnl_analytics:123456@host.docker.internal:5432/sgnl}
```

**app/requirements.txt:**
```
sqlalchemy>=2.0.0
user-agent>=0.1.10
psycopg2-binary>=2.9.0
```

### Database Schema

```sql
-- visitor_logs table
CREATE TABLE visitor_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    user_agent TEXT,
    device_type VARCHAR(20),
    country VARCHAR(50),
    city VARCHAR(100),
    referrer TEXT,
    landing_page VARCHAR(500),
    created_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    total_time_seconds FLOAT DEFAULT 0.0
);

-- page_views table
CREATE TABLE page_views (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    path VARCHAR(500) NOT NULL,
    query_params TEXT,
    time_on_page FLOAT,
    created_at TIMESTAMP NOT NULL
);

-- analytics_events table
CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data TEXT,
    created_at TIMESTAMP NOT NULL
);
```

### Cost

- **PostgreSQL**: Free (you already have it)
- **Storage**: Minimal (few KB per visitor)
- **Dependencies**: All open source
- **Total**: $0/month

### Documentation

- **Full documentation**: `docs/ANALYTICS.md`
- **Implementation summary**: `ANALYTICS_IMPLEMENTATION.md`

### Status

✅ Database configured
✅ Tables created
✅ API routes registered
✅ Middleware active
✅ JavaScript loaded
⚠️ Session creation needs debugging
⚠️ Visitor recording not working yet

---

**To fix session creation**, run the tests above and check logs for errors.
