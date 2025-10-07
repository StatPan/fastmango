# Database Schema Documentation

Generated on: 2025-10-07T22:03:42.005429

## Database Information

- **Version**: SQLite 3.49.1
- **Table Count**: 2

## Models

### User

**Table**: `user`

**Description**: No description available

#### Columns

| Name | Type | Nullable | Primary Key | Unique | Default | Foreign Key |
|------|------|----------|-------------|--------|---------|-------------|
| id | INTEGER | ✗ | ✓ | ✗ | - | - |
| username | VARCHAR | ✗ | ✗ | ✓ | - | - |
| email | VARCHAR | ✗ | ✗ | ✓ | - | - |
| password_hash | VARCHAR | ✓ | ✗ | ✗ | - | - |
| is_active | BOOLEAN | ✗ | ✗ | ✗ | ScalarElementColumnDefault(True) | - |
