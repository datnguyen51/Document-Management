class DocumentStatus(object):
    INITIALIZATION = 'init'  # Khoi tao
    PROCESS = 'process'  # Dang xu ly
    PENDING = 'pending'  # Cho xu ly
    RECEIVE = 'receive'  # Tiep nhan
    REJECT = 'reject'  # Tu choi
    FINISH = 'finish'  # Hoan thanh
    WORKING = 'working'  # Dang lam
    EXPIRE = 'expire'


class ReportStatus(object):
    REVIEW = 'review'  # Khoi tao
    REJECT = 'reject'  # Dang xu ly
    APPROVE = 'approve'  # Cho xu ly
    FINISH = 'finish'  # Hoan thanh


class UserRoleStatus(object):
    STAFF = 'staff'
    MANAGER = 'manager'
    ADMIN = 'admin'
    STAFF_LEAD = 'staff_lead'
