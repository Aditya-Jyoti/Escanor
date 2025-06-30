-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  unique_code VARCHAR(3) NOT NULL UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create pastes table
CREATE TABLE IF NOT EXISTS pastes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  slug VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  language VARCHAR(50) NOT NULL DEFAULT 'plaintext',
  is_public BOOLEAN NOT NULL DEFAULT true,
  password VARCHAR(255),
  view_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, slug)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_unique_code ON users(unique_code);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_pastes_user_id ON pastes(user_id);
CREATE INDEX IF NOT EXISTS idx_pastes_slug ON pastes(slug);
CREATE INDEX IF NOT EXISTS idx_pastes_created_at ON pastes(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_pastes_public ON pastes(is_public);

