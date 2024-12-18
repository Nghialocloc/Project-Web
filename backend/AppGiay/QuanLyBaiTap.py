from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SinhVien, GiangVien
from .models import LopHoc, ThanhVienLop
from .models import BaiTap, BaiLam
from .serializers import UserAccountSerializer, SinhVienSerializer
from .serializers import LopHocSerializer, ThanhVienLopSerializer
from .serializers import BaiTapSerializer, BaiLamSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime

User = get_user_model()

def is_valid_param(param) :
    return param != " " and param is not None and param != ""


def id_generator (size, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ManageAssignment(APIView):

    permission_classes = (permissions.AllowAny, )

    # Create Assignment
    def post(self, request, format=None):
        try:
            # Lấy dữ liệu từ request
            data = request.data
            user = request.user

            # Kiểm tra quyền của giáo viên
            if not user.is_teacher:
                return Response(
                    {
                        'code': 1009,
                        'message': 'User does not have necessary permission'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # Kiểm tra id lớp học (idlop) có tồn tại hay không
            idlophoc = data.get('idlophoc')
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return Response(
                    {
                        'code': 1004,
                        'message': 'Class ID not found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # Tạo ID bài tập duy nhất
            while True:
                idbaitap = id_generator()
                if not BaiTap.objects.filter(idbaitap=idbaitap).exists():
                    break

            # Lấy các trường dữ liệu đầu vào
            tenbaitap = data.get('tenbaitap')
            mota = data.get('mota')
            deadline = data.get('deadline')
            filebaitap = data.get('filebaitap')

            # Kiểm tra tên bài tập hợp lệ
            if not is_valid_param(tenbaitap) or len(tenbaitap) > 50:
                return Response(
                    {
                        'code': 1004,
                        'message': 'Invalid assignment name. Must be less than 50 characters.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra hạn nộp bài hợp lệ
            if not is_valid_param(deadline):
                return Response(
                    {
                        'code': 1004,
                        'message': 'Deadline is required.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
            if deadline_date < datetime.datetime.now():
                    return Response(
                        {
                            'code': 1004,
                            'message': 'Deadline must not be in the past.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )                

            # Tạo và lưu bài tập mới vào database
            baitap = BaiTap(idbaitap = idbaitap, idlop_id=idlophoc, tenbaitap = tenbaitap, mota = mota, filebaitap = filebaitap, 
                            deadline = deadline_date, create_day = datetime.datetime.now())

            # Serialize dữ liệu và phản hồi kết quả
            serializer = BaiTapSerializer(baitap)
            return Response(
                {
                    'code': 1000,
                    'message': 'Assignment created successfully.',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    # Edit Assignment
    def put(self, request):
        try: 
            # Kiểm tra quyền của người dùng (phải là giáo viên)
            user = request.user
            if not user.is_teacher:
                return Response(
                    {
                        'code': 1009,
                        'message': 'User does not have necessary permission'
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Lấy dữ liệu từ request
            data = request.data
            idbaitap = data.get('idbaitap')

            # Kiểm tra ID bài tập có được cung cấp không
            if not is_valid_param(idbaitap):
                return Response(
                    {
                        'code': 1004,
                        'message': 'Invalid assignment ID. Please check and add input'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra bài tập có tồn tại không
            if BaiTap.objects.filter(idbaitap=idbaitap).count() == 0:
                return Response(
                    {
                        'code': 9992,
                        'message': 'Assignment not found. Please try again.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            baitap = BaiTap.objects.get(idbaitap=idbaitap)

            # Lấy các trường dữ liệu mới
            tenbaitap = data.get('tenbaitap')
            mota = data.get('mota')
            deadline = data.get('deadline')
            filebaitap = data.get('filebaitap')

            # Serialize dữ liệu cũ để kiểm tra thay đổi
            baitap_seria = BaiTapSerializer(baitap)
            old_tenbaitap = baitap_seria.data.get('tenbaitap')
            old_mota = baitap_seria.data.get('mota')
            old_han_nop = baitap_seria.data.get('han_nop')
            old_filebaitap = baitap_seria.data.get('filebaitap')

            # Kiểm tra dữ liệu mới có thay đổi không
            if (old_tenbaitap == tenbaitap and old_mota == mota and old_han_nop == deadline and old_filebaitap == filebaitap):
                return Response(
                    {
                        'code': 1012,
                        'message': 'No information has been modified'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra độ dài mô tả
            if len(mota) > 200:
                return Response(
                    {
                        'code': 1013,
                        'message': 'The description is too long for the input field.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra ngày deadline moi hợp lệ
            if is_valid_param(deadline_date):
                deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
                if deadline_date < datetime.datetime.now():
                    return Response(
                        {
                            'code': 1004,
                            'message': 'Deadline must not be in the past.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Cập nhật dữ liệu mới cho bài tập
            if is_valid_param(tenbaitap):
                baitap.tenbaitap = tenbaitap
            if is_valid_param(mota):
                baitap.mota = mota
            if is_valid_param(deadline):
                baitap.deadline = deadline
            if is_valid_param(filebaitap):
                baitap.filebaitap = filebaitap
            baitap.save()

            # Serialize lại dữ liệu đã cập nhật
            updated_serializer = BaiTapSerializer(baitap)

            return Response(
                {
                    'code': 1000,
                    'message': 'Update success',
                    'Updated assignment info': updated_serializer.data
                },
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Detele Assignment
    def delete(self, request):
        try:
            # Kiểm tra quyền của người dùng (phải là giáo viên)
            user = request.user
            if not user.is_teacher:
                return Response(
                    {
                        'code': 1009,
                        'message': 'User does not have necessary permission'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # Lấy ID bài tập từ request
            data = request.data
            idbaitap = data.get('idbaitap')

            # Kiểm tra ID bài tập có được cung cấp không
            if not is_valid_param(idbaitap):
                return Response(
                    {
                        'code': 1004,
                        'message': 'Missing assignment ID. Please add input'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra bài tập có tồn tại không
            if BaiTap.objects.filter(idbaitap=idbaitap).count() == 0:
                return Response(
                    {
                        'code': 9992,
                        'message': 'Assignment not found. Please try again.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # Kiểm tra xem bài tập có sinh viên nộp bài hay không
            if BaiLam.objects.filter(idbaitap=idbaitap).exists():
                return Response(
                    {
                        'code': 1014,
                        'message': 'Cannot delete assignment. Students have already submitted their work.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Xóa bài tập
            baitap = BaiTap.objects.get(idbaitap=idbaitap)
            baitap.delete()

            return Response(
                {
                    'code': 1000,
                    'message': 'Assignment deleted successfully'
                },
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class ManageHomework(APIView):

    permission_classes = (permissions.AllowAny, )

    #Get homework list
    def get(self, request):
        """
        Lấy danh sách bài nộp của sinh viên theo ID bài tập.
        Chỉ giáo viên được phép truy cập.
        """
        try:
            # Kiểm tra quyền của người dùng (phải là giáo viên)
            user = request.user
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data
            # Lấy ID bài tập từ query parameters
            idbaitap = data.get('idbaitap')

            # Kiểm tra ID bài tập hợp lệ
            if not is_valid_param(idbaitap):
                return Response(
                    {
                        "code": 1004, 
                        "message": "Missing assignment ID."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra bài tập có tồn tại không
            if BaiTap.objects.filter(idbaitap=idbaitap).count() == 0:
                return Response(
                    {
                        "code": 1005, 
                        "message": "Assignment not found. Please check input again."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # Lấy danh sách bài nộp cho bài tập
            submissions = BaiLam.objects.filter(idbaitap=idbaitap)
            submissions_seria = BaiLamSerializer(submissions, many=True)
            idsinhvien = submissions_seria.data.get('idsinhvien')
            ngaynop = submissions_seria.data.get('ngaynop')
            diem = submissions_seria.data.get('diem')

            list_homework = {
                " Id sinh vien" : idsinhvien,
                " Thoi gian nop" : ngaynop,
                " Diem da cham" : diem
            }

            return Response(
                {
                    "code": 1000, 
                    "message": "Submissions retrieved successfully.", 
                    "data": list_homework
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"code": 5000, "message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Grade homework
    def put(self, request):
        """
        Chấm điểm bài nộp của sinh viên.
        Chỉ giáo viên được phép thực hiện.
        """
        try:
            # Kiểm tra quyền của người dùng (phải là giáo viên)
            user = request.user
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Lấy dữ liệu từ request
            data = request.data
            idbailam = data.get('idbailam')
            diem = data.get('diem')

            # Kiểm tra ID bài nộp hợp lệ
            if not is_valid_param(idbailam):
                return Response(
                    {
                        "code": 1004, 
                        "message": "Missing submission ID. "
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Kiểm tra bài nộp có tồn tại không
            try:
                submission = BaiLam.objects.get(idbailam = idbailam)
            except BaiLam.DoesNotExist:
                return Response(
                    {
                        "code": 1005, 
                        "message": "Submission not found. Please add id"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # Kiểm tra điểm hợp lệ (từ 0 đến 10)
            if diem is None or not (0 <= float(diem) <= 10):
                return Response(
                    {
                        "code": 1006, 
                        "message": "Invalid score. Score must be between 0 and 10."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Cập nhật điểm cho bài nộp
            submission.diem = diem
            submission.save()

            # Serialize kết quả
            serializer = BaiLamSerializer(submission)
            return Response(
                {
                    "code": 1000, 
                    "message": "Score updated successfully.", 
                    "data": serializer.data
                },
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"code": 5000, "message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SubmitHomework(APIView):

    permission_classes = (permissions.AllowAny, )

    #Submit homework
    def post(self, request):
        try:
            user = request.user
            if (user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data
            idbaitap = data.get('idbaitap')
            filebaigiai = data.get('filebaigiai')  # File bài làm
            description = data.get('description')  # Mô tả văn bản bài làm

            # 1. Kiểm tra ID bài tập có hợp lệ không
            if BaiTap.objects.filter(idbaitap = idbaitap).count() == 0:
                return Response(
                    {
                        "code": 1004, 
                        "message": "Assignment id not found. Please check input again."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # 2. Lay ID sinh viên 
            sinhvien = SinhVien.objects.get(id = user.id)
            sinhvien_seria = SinhVienSerializer(sinhvien)
            idsinhvien = sinhvien_seria.data.get('idsinhvien')

            # 3. Lấy thông tin bài tập để kiểm tra deadline
            baitap = BaiTap.objects.get(idbaitap = idbaitap)
            baitap_seria = BaiTapSerializer(baitap)
            deadline = baitap_seria.data.get('deadline')
            ngaynop = str(datetime.datetime.now())

            if deadline < ngaynop:
                return Response(
                    {
                        "code": 1006, 
                        "message": "Deadline has passed so submission is not allowed."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 4. Kiểm tra xem sinh viên đã nộp bài chưa
            if BaiLam.objects.filter(idbaitap = idbaitap, idsinhvien = idsinhvien).exists():
                return Response(
                    {
                        "code": 1014, 
                        "message": "You have already submitted this assignment."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 5. Phân biệt 2 trường hợp: Nộp file và nộp văn bản
            if filebaigiai:
                # Trường hợp nộp file
                while True:
                    idbailam = id_generator(size= 8)
                    if (BaiLam.objects.filter(idbailam = idbailam).count() == 0):
                        break
                bailam = BaiLam(idbailam=idbailam, idbaitap=baitap, idsinhvien = sinhvien, filebaigiai = filebaigiai, 
                                description=description, ngaynop = ngaynop)
                bailam.save()
                return Response(
                    {
                        "code": 1000,
                        "message": "File submission successful.",
                    },
                    status=status.HTTP_201_CREATED
                )

            elif is_valid_param(description):
                # Trường hợp nộp văn bản
                while True:
                    idbailam = id_generator(size= 8)
                    if (BaiLam.objects.filter(idbailam = idbailam).count() == 0):
                        break
                bailam = BaiLam(idbailam=idbailam, idbaitap=baitap, idsinhvien = sinhvien, filebaigiai = filebaigiai, 
                                description=description, ngaynop = ngaynop)
                bailam.save()
                return Response(
                    {
                        "code": 1001,
                        "message": "Text submission successful.",
                    },
                    status=status.HTTP_201_CREATED
                )

            else:
                # Không có file và không có mô tả
                return Response(
                    {
                        "code": 1007,
                        "message": "Either file or description must be provided."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Edit homework


    #Delete homework


class GetAssignmemntList(APIView):

    permission_classes = (permissions.AllowAny, )

    #GetAssignmentList

    





