-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS dummy_portfolio;
USE dummy_portfolio;

-- Create user table
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create STOCK table to store Yahoo Finance data
CREATE TABLE IF NOT EXISTS STOCK (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    ticker_symbol VARCHAR(20) UNIQUE NOT NULL,
    current_price DECIMAL(10, 2),
    market_sector VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create portfolio table for users to save their stocks
CREATE TABLE IF NOT EXISTS portfolio (
    portfolio_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ticker_symbol VARCHAR(20) NOT NULL,
    quantity INT DEFAULT 1,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    UNIQUE (user_id, ticker_symbol)
);

-- Insert some sample data for testing with plain text password
INSERT INTO user (username, email, password_hash) VALUES
('testuser', 'test@example.com', 'password123');
