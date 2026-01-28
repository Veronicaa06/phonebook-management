from storage import ContactStorage

class ContactService:
    """
    Xử lý logic nghiệp vụ liên quan đến danh bạ.
    Tách biệt với UI và Storage.
    """

    def __init__(self):
        # Khởi tạo storage để thao tác DB
        self.repo = ContactStorage()

    def add_contact(self, name, phone, email, user_id):
        """
        Thêm liên hệ mới.
        - name, phone: bắt buộc
        - email: tùy chọn
        - user_id: ID của user hiện tại
        Trả về: (True/False, Thông báo)
        """
        if not name or not phone:
            return False, "Name và Phone không được trống."

        try:
            self.repo.add_contact(name, phone, email, user_id)
            return True, "Thêm thành công!"
        except Exception as e:
            # Debug lỗi DB
            return False, f"Lỗi khi thêm contact: {e}"

    def edit_contact(self, contact_id, name, phone, email):
        """
        Chỉnh sửa liên hệ theo ID.
        - Kiểm tra tên không trống
        - contact_id phải tồn tại trong DB
        Trả về: (True/False, Thông báo)
        """
        if not name:
            return False, "Name không được trống"

        try:
            updated = self.repo.update_contact(contact_id, name, phone, email)
            if updated:
                return True, "Cập nhật thành công!"
            else:
                # Nếu không có bản ghi nào bị update
                return False, f"Không tìm thấy contact ID: {contact_id}"
        except Exception as e:
            # Debug lỗi DB
            return False, f"Lỗi khi cập nhật contact: {e}"

    def search(self, keyword, user_id):
        """
        Tìm kiếm liên hệ theo từ khóa.
        Trả về list dictionary kết quả.
        """
        try:
            return self.repo.search_contact(keyword, user_id)
        except Exception as e:
            print(f"Lỗi khi tìm kiếm: {e}")
            return []

    def list_contacts(self, user_id):
        """
        Liệt kê tất cả liên hệ của user.
        Trả về list dictionary.
        """
        try:
            return self.repo.get_contacts(user_id)
        except Exception as e:
            print(f"Lỗi khi lấy danh bạ: {e}")
            return []
        
    def delete_contact(self, contact_id):
        """
        Xóa liên hệ theo ID.
        Trả về: (True/False, message)
        """
        try:
            deleted = self.repo.delete_contact(contact_id)
            if deleted:
                return True, "Xóa thành công!"
            else:
                return False, f"Không tìm thấy contact ID: {contact_id}"
        except Exception as e:
            return False, f"Lỗi khi xóa contact: {e}"