"""
Efficient Data Management System
Handles data archiving, compression, and cleanup without losing context
"""

import sqlite3
import json
import os
import gzip
import shutil
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("DEAR.DataManager")

class DataManager:
    def __init__(self, db_path: str = "backend/data/memory.db"):
        self.db_path = db_path
        self.archive_dir = "backend/data/archives"
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        
        # Create archives directory
        os.makedirs(self.archive_dir, exist_ok=True)
        
        logger.info("Data Manager initialized")
    
    def get_database_size(self):
        """Get current database size in MB"""
        if os.path.exists(self.db_path):
            size_bytes = os.path.getsize(self.db_path)
            size_mb = size_bytes / (1024 * 1024)
            return size_mb
        return 0
    
    def get_conversation_count(self):
        """Get total number of conversations"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM conversation")
        count = cursor.fetchone()[0]
        return count
    
    def get_old_conversations(self, days_old: int = 30):
        """Get conversations older than specified days"""
        cursor = self.conn.cursor()
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        cursor.execute("""
            SELECT id, role, content, timestamp 
            FROM conversation 
            WHERE timestamp < ?
            ORDER BY timestamp ASC
        """, (cutoff_date.isoformat(),))
        
        return cursor.fetchall()
    
    def archive_old_conversations(self, days_old: int = 30, compress: bool = True):
        """
        Archive old conversations to compressed file
        Keeps recent conversations for context
        """
        logger.info(f"Archiving conversations older than {days_old} days...")
        
        old_convos = self.get_old_conversations(days_old)
        
        if not old_convos:
            logger.info("No old conversations to archive")
            return {
                "archived": 0,
                "file": None,
                "size_saved": 0
            }
        
        # Create archive data
        archive_data = {
            "archived_date": datetime.now().isoformat(),
            "cutoff_days": days_old,
            "conversation_count": len(old_convos),
            "conversations": []
        }
        
        for conv_id, role, content, timestamp in old_convos:
            archive_data["conversations"].append({
                "id": conv_id,
                "role": role,
                "content": content,
                "timestamp": timestamp
            })
        
        # Generate archive filename
        archive_filename = f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        if compress:
            archive_filename += ".gz"
            archive_path = os.path.join(self.archive_dir, archive_filename)
            
            # Write compressed JSON
            with gzip.open(archive_path, 'wt', encoding='utf-8') as f:
                json.dump(archive_data, f, indent=2)
        else:
            archive_path = os.path.join(self.archive_dir, archive_filename)
            
            # Write regular JSON
            with open(archive_path, 'w', encoding='utf-8') as f:
                json.dump(archive_data, f, indent=2)
        
        # Delete archived conversations from database
        cursor = self.conn.cursor()
        cutoff_date = datetime.now() - timedelta(days=days_old)
        cursor.execute("DELETE FROM conversation WHERE timestamp < ?", 
                      (cutoff_date.isoformat(),))
        self.conn.commit()
        
        # Calculate space saved
        archive_size = os.path.getsize(archive_path) / (1024 * 1024)  # MB
        
        # Vacuum database to reclaim space
        cursor.execute("VACUUM")
        
        logger.info(f"Archived {len(old_convos)} conversations to {archive_filename}")
        logger.info(f"Archive size: {archive_size:.2f} MB")
        
        return {
            "archived": len(old_convos),
            "file": archive_path,
            "size_mb": archive_size,
            "compressed": compress
        }
    
    def restore_from_archive(self, archive_file: str):
        """Restore conversations from archive file"""
        logger.info(f"Restoring from archive: {archive_file}")
        
        archive_path = os.path.join(self.archive_dir, archive_file)
        
        if not os.path.exists(archive_path):
            logger.error(f"Archive file not found: {archive_file}")
            return {"restored": 0, "error": "File not found"}
        
        # Read archive (handle both compressed and uncompressed)
        try:
            if archive_file.endswith('.gz'):
                with gzip.open(archive_path, 'rt', encoding='utf-8') as f:
                    archive_data = json.load(f)
            else:
                with open(archive_path, 'r', encoding='utf-8') as f:
                    archive_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to read archive: {str(e)}")
            return {"restored": 0, "error": str(e)}
        
        # Restore conversations
        cursor = self.conn.cursor()
        restored = 0
        
        for conv in archive_data["conversations"]:
            try:
                cursor.execute("""
                    INSERT INTO conversation (role, content, timestamp)
                    VALUES (?, ?, ?)
                """, (conv["role"], conv["content"], conv["timestamp"]))
                restored += 1
            except Exception as e:
                logger.warning(f"Failed to restore conversation {conv['id']}: {str(e)}")
        
        self.conn.commit()
        
        logger.info(f"Restored {restored} conversations from archive")
        
        return {
            "restored": restored,
            "total_in_archive": len(archive_data["conversations"])
        }
    
    def list_archives(self):
        """List all archive files"""
        archives = []
        
        if not os.path.exists(self.archive_dir):
            return archives
        
        for filename in os.listdir(self.archive_dir):
            if filename.startswith('archive_') and (filename.endswith('.json') or filename.endswith('.json.gz')):
                filepath = os.path.join(self.archive_dir, filename)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                
                archives.append({
                    "filename": filename,
                    "size_mb": round(size_mb, 2),
                    "created": datetime.fromtimestamp(os.path.getctime(filepath)).isoformat(),
                    "compressed": filename.endswith('.gz')
                })
        
        return sorted(archives, key=lambda x: x["created"], reverse=True)
    
    def create_summary_context(self, limit: int = 100):
        """
        Create summarized context from old conversations
        Keeps important information without full conversation history
        """
        cursor = self.conn.cursor()
        
        # Get old conversations
        cursor.execute("""
            SELECT role, content, timestamp 
            FROM conversation 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        conversations = cursor.fetchall()
        
        # Extract key topics and information
        summary = {
            "total_conversations": len(conversations),
            "date_range": {
                "oldest": conversations[-1][2] if conversations else None,
                "newest": conversations[0][2] if conversations else None
            },
            "topics": [],
            "user_preferences": []
        }
        
        # Simple keyword extraction (can be enhanced with NLP)
        keywords = {}
        for role, content, timestamp in conversations:
            words = content.lower().split()
            for word in words:
                if len(word) > 5:  # Only meaningful words
                    keywords[word] = keywords.get(word, 0) + 1
        
        # Get top keywords
        top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:20]
        summary["topics"] = [word for word, count in top_keywords]
        
        return summary
    
    def smart_cleanup(self, max_size_mb: int = 50, keep_recent_days: int = 7):
        """
        Smart cleanup that maintains context while reducing size
        
        Strategy:
        1. Keep all conversations from last N days (default 7)
        2. Archive older conversations
        3. Create summary context from archived data
        4. Compress archives
        """
        logger.info(f"Starting smart cleanup (max size: {max_size_mb} MB, keep recent: {keep_recent_days} days)")
        
        current_size = self.get_database_size()
        
        if current_size < max_size_mb:
            logger.info(f"Database size ({current_size:.2f} MB) is within limit")
            return {
                "cleanup_needed": False,
                "current_size_mb": current_size,
                "max_size_mb": max_size_mb
            }
        
        # Archive old conversations
        archive_result = self.archive_old_conversations(
            days_old=keep_recent_days,
            compress=True
        )
        
        # Create summary context
        summary = self.create_summary_context()
        
        # Save summary
        summary_path = os.path.join(self.archive_dir, "context_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        new_size = self.get_database_size()
        space_saved = current_size - new_size
        
        logger.info(f"Cleanup complete. Space saved: {space_saved:.2f} MB")
        
        return {
            "cleanup_needed": True,
            "archived_conversations": archive_result["archived"],
            "archive_file": archive_result["file"],
            "old_size_mb": current_size,
            "new_size_mb": new_size,
            "space_saved_mb": space_saved,
            "summary_created": True
        }
    
    def get_stats(self):
        """Get database statistics"""
        return {
            "database_size_mb": round(self.get_database_size(), 2),
            "total_conversations": self.get_conversation_count(),
            "archives": self.list_archives(),
            "archive_count": len(self.list_archives())
        }

# Example usage
if __name__ == "__main__":
    manager = DataManager()
    
    print("📊 Database Statistics:")
    stats = manager.get_stats()
    print(f"  Size: {stats['database_size_mb']} MB")
    print(f"  Conversations: {stats['total_conversations']}")
    print(f"  Archives: {stats['archive_count']}")
    
    print("\n🗜️ Running smart cleanup...")
    result = manager.smart_cleanup(max_size_mb=50, keep_recent_days=7)
    
    if result["cleanup_needed"]:
        print(f"  ✅ Archived {result['archived_conversations']} conversations")
        print(f"  💾 Space saved: {result['space_saved_mb']:.2f} MB")
    else:
        print("  ✅ No cleanup needed")
