from typing import Dict, List, Optional


class Testimony:
    TABLE = "testimonies"

    @staticmethod
    def get_featured(db, limit: int = 5) -> List[Dict]:
        try:
            response = (
                db.client.table(Testimony.TABLE)
                .select("title, author, category, branch, anonymous")
                .in_("status", ["featured", "approved"])
                .order("status", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data or []
        except Exception as e:
            print(f"[ERROR] Testimony.get_featured: {e}")
            return []

    @staticmethod
    def save(db, name: str, title: str, category: str, content: str, branch: str, is_member: bool, is_anonymous: bool) -> Optional[Dict]:
        try:
            author = "Anonymous" if is_anonymous else name
            response = (
                db.client.table(Testimony.TABLE)
                .insert({
                    "author": author,
                    "title": title,
                    "category": category,
                    "content": content,
                    "branch": branch,
                    "is_member": is_member,
                    "anonymous": is_anonymous,
                    "status": "pending",
                })
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[ERROR] Testimony.save: {e}")
            return None
